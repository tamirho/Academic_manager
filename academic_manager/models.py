from academic_manager import db


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    enrollment = db.relationship('Enrollment', backref='student', lazy=True)

    def __init__(self, user_name, email, password):
        self.user_name = user_name
        self.email = email
        self.password = password

    def __repr__(self):
        return f"Student('{self.user_name}','{self.email}','{self.password}')"


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    course = db.relationship('Course', backref='lecturer', lazy=True)

    def __init__(self, user_name, email, password):
        self.user_name = user_name
        self.email = email
        self.password = password

    def __repr__(self):
        return f"Teacher('{self.user_name}','{self.email}','{self.password}')"


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(30), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)
    enrollment = db.relationship('Enrollment', backref='course', lazy=True)

    def __init__(self, course_name, teacher_id):
        self.course_name = course_name
        self.teacher_id = teacher_id

    def __repr__(self):
        return f"Course('{self.course_name}','{self.teacher_id}')"


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



