import os
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from academic_manager.extensions import db, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    __table_name__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    profile_img = db.Column(db.String(30), nullable=False, default='default/default.jpg')
    gender = db.Column(db.String(1), nullable=False)  # ['m','f']
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    last_seen = db.Column(db.DateTime, nullable=False, default=datetime.now)
    role = db.Column(db.String(100), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': role
    }

    def __init__(self, email, first, last, password, gender):
        self.email = email.lower()
        self.first_name = first
        self.last_name = last
        self.password = password
        self.gender = gender

    def __repr__(self):
        return f"User('{self.email}','{self.full_name}','{self.password}')"

    @property
    def full_name(self):
        return f"{self.first_name.capitalize()} {self.last_name.capitalize()}"

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_teacher(self):
        return self.role == 'teacher'

    @property
    def is_student(self):
        return self.role == 'student'

    def update_last_seen(self):
        self.last_seen = datetime.now()
        db.session.commit()

    def get_reset_password_token(self, expires_sec=1800):
        ser = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return ser.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        ser = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = ser.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


class Admin(User):
    __table_name__ = 'admin'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'admin',
    }

    def __init__(self, email, first, last, hashed_password, gender):
        User.__init__(self, email, first, last, hashed_password, gender)
        if gender == 'Male':
            self.profile_img = "default/teacher-man-profile.jpg"
        else:
            self.profile_img = "default/teacher-woman-profile.jpg"

    def __repr__(self):
        return f"Admin('{self.email}')"

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class Teacher(User):
    __table_name__ = 'teacher'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    approved = db.Column(db.Boolean, default=False, nullable=False)

    # define relationships
    course = db.relationship('Course', backref='lecturer', lazy=True)
    tasks = db.relationship('Task', backref='author', lazy=True)

    __mapper_args__ = {
        'polymorphic_identity': 'teacher',
    }

    def __init__(self, email, first, last, hashed_password, gender):
        User.__init__(self, email, first, last, hashed_password, gender)
        if gender == 'Male':
            self.profile_img = "default/teacher-man-profile.jpg"
        else:
            self.profile_img = "default/teacher-woman-profile.jpg"

    def __repr__(self):
        return f"Teacher('{self.email}','{self.full_name}','{self.gender}','{self.approved}')"

    def delete_from_db(self):
        for course in Course.query.filter(Course.teacher_id == self.id):
            course.delete_from_db()
        db.session.delete(self)
        db.session.commit()


class Student(User):
    __table_name__ = 'student'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    enrollment = db.relationship('Enrollment', backref='student', lazy=True)

    __mapper_args__ = {
        'polymorphic_identity': 'student',
    }

    def __init__(self, email, first, last, hashed_password, gender):
        User.__init__(self, email, first, last, hashed_password, gender)
        if gender == 'Male':
            self.profile_img = "default/man-profile.jpg"
        else:
            self.profile_img = "default/woman-profile.jpg"

    def __repr__(self):
        return f"Student('{self.email}','{self.full_name}','{self.gender}')"

    def delete_from_db(self):
        Enrollment.query.filter(Enrollment.student_id == self.id).delete()
        db.session.delete(self)
        db.session.commit()

    def avg(self):
        grade_list = [int(enroll.grade) for enroll in self.enrollment if enroll.grade]
        if grade_list:
            return sum(grade_list) / len(grade_list)
        else:
            return 0

    def get_courses_id_lst(self):
        return [enroll.course_id for enroll in self.enrollment]


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(30), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)

    # define relationships
    enrollment = db.relationship('Enrollment', backref='course', lazy=True)
    task = db.relationship('Task', backref='course', lazy=True)

    def __init__(self, course_name, teacher_id):
        self.course_name = course_name
        self.teacher_id = teacher_id

    def __repr__(self):
        return f"Course('{self.course_name}','{self.teacher_id}')"

    def delete_from_db(self):
        Enrollment.query.filter(Enrollment.course_id == self.id).delete()

        # Remove all Tasks and files
        for task in Task.query.filter(Task.course_id == self.id):
            task.delete_from_db()

        self.remove_directory()
        db.session.delete(self)
        db.session.commit()

    def create_directory(self):
        directory = str(self.id)
        parent_dir = "static/uploads"
        path = os.path.join(current_app.root_path, parent_dir, directory)

        try:
            os.mkdir(path)
        except FileExistsError as error:
            print(error)
        except FileNotFoundError as error:
            print(error)
            return None

        return path

    def remove_directory(self):
        parent_dir = "static/uploads"
        path = os.path.join(current_app.root_path, parent_dir, str(self.id))
        try:
            os.rmdir(path)
            print(f"Directory {path} has been removed successfully")
        except OSError as error:
            print(error)
            print(f"Directory {path} can not be removed")


class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    grade = db.Column(db.Integer, nullable=True)

    # define relationships
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)

    def __init__(self, course_id, student_id):
        self.course_id = course_id
        self.student_id = student_id

    def __repr__(self):
        return f"Enrollment('{self.course_id}','{self.student_id}','{self.grade}')"

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    update_time = db.Column(db.DateTime, nullable=True)

    # define relationships
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)
    files = db.relationship('File', backref='task', lazy=True)

    def __init__(self, title, content, course_id, teacher_id):
        self.title = title
        self.content = content
        self.course_id = course_id
        self.teacher_id = teacher_id

    def __repr__(self):
        if self.update_time:
            return f"Task('{self.title}','{self.date_posted}','{self.update_time}')"
        else:
            return f"Task('{self.title}','{self.date_posted}')"

    def delete_from_db(self):
        for file in File.query.filter(File.task_id == self.id):
            file.delete_from_db()
        db.session.delete(self)
        db.session.commit()

    def update(self, new_title, new_content):
        self.title = new_title
        self.content = new_content
        self.add_update_time()
        db.session.commit()

    def add_update_time(self):
        self.update_time = datetime.now()


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    # define relationships
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)

    def __init__(self, name, task_id):
        self.name = name
        self.task_id = task_id

    def __repr__(self):
        return f"File('{self.name}','{self.task_id}')"

    @property
    def path(self):
        return f"{self.task.course_id}/{self.name}"

    def delete_from_db(self):
        self.remove_file()
        db.session.delete(self)
        db.session.commit()

    def remove_file(self):
        parent_dir = "static/uploads"
        path = os.path.join(current_app.root_path, parent_dir, self.path)
        try:
            os.remove(path)
            print(f"File {path} has been removed successfully")
        except OSError as error:
            print(error)
            print(f"File {path} can not be removed")
