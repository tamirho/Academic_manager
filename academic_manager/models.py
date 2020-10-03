from academic_manager import db
from datetime import datetime
from functools import reduce


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    last_seen = db.Column(db.DateTime, nullable=False, default=datetime.now)
    enrollment = db.relationship('Enrollment', backref='student', lazy=True)

    def __init__(self, user_name, email, password):
        self.user_name = user_name
        self.email = email
        self.password = password

    def __repr__(self):
        return f"Student('{self.user_name}','{self.email}','{self.password}')"

    def delete_from_db(self):
        Enrollment.query.filter(Enrollment.student_id == self.id).delete()
        db.session.delete(self)
        db.session.commit()

    def get_courses_id_lst(self):
        return [enroll.course_id for enroll in self.enrollment]

    def avg(self):
        grade_list = [int(enroll.grade) for enroll in self.enrollment if enroll.grade]
        if grade_list:
            return reduce(lambda a, b: a + b, grade_list) / len(grade_list)
        else:
            return 0


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    last_seen = db.Column(db.DateTime, nullable=False, default=datetime.now)
    approved = db.Column(db.Boolean, default=False, nullable=False)
    course = db.relationship('Course', backref='lecturer', lazy=True)

    def __init__(self, user_name, email, password):
        self.user_name = user_name
        self.email = email
        self.password = password

    def __repr__(self):
        return f"Teacher('{self.user_name}','{self.email}','{self.password}','{self.approved}')"

    def delete_from_db(self):
        for course in Course.query.filter(Course.teacher_id == self.id):
            course.delete_from_db()
        db.session.delete(self)
        db.session.commit()


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(30), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)
    enrollment = db.relationship('Enrollment', backref='course', lazy=True)
    task = db.relationship('Task', backref='course', lazy=True)

    def __init__(self, course_name, teacher_id):
        self.course_name = course_name
        self.teacher_id = teacher_id

    def __repr__(self):
        return f"Course('{self.course_name}','{self.teacher_id}')"

    def delete_from_db(self):
        Enrollment.query.filter(Enrollment.course_id == self.id).delete()
        Task.query.filter(Task.course_id == self.id).delete()
        db.session.delete(self)
        db.session.commit()


class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    grade = db.Column(db.Integer, nullable=True)

    def __init__(self, course_id, student_id):
        self.course_id = course_id
        self.student_id = student_id

    def __repr__(self):
        return f"Enrollment('{self.course_id}','{self.student_id}','{self.grade}')"

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __init__(self, user_name, password):
        self.user_name = user_name
        self.password = password

    def __repr__(self):
        return f"Admin('{self.user_name}','{self.password}')"

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    update_time = db.Column(db.DateTime, nullable=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)

    def __init__(self, title, content, course_id):
        self.title = title
        self.content = content
        self.course_id = course_id
        self.date_posted = datetime.now()

    def __repr__(self):
        if self.update_time:
            return f"Task('{self.title}','{self.date_posted}','{self.update_time}')"
        else:
            return f"Task('{self.title}','{self.date_posted}')"

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, new_title, new_content):
        self.title = new_title
        self.content = new_content
        self.add_update_time()
        db.session.commit()

    def add_update_time(self):
        self.update_time = datetime.now()
