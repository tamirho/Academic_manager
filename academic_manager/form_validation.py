from academic_manager.models import Student,Teacher
from academic_manager import db


def sign_up_validation(user_name, user_email, user_password, password_confirmation):
    messages = []
    if not validate_user_name(user_name):
        messages.append("username already exist")
    if not validate_password(user_password, password_confirmation):
        messages.append("The passwords are not equal")
    if not validate_email(user_email):
        messages.append("email already exist")

    if not messages:
        return True, messages
    else:
        return False, messages


def validate_user_name(user_name):
    student = Student.query.filter_by(user_name=user_name).first()
    teacher = Teacher.query.filter_by(user_name=user_name).first()
    if student or teacher:
        return False
    else:
        return True


def validate_password(user_password, password_confirmation):
    if user_password != password_confirmation:
        return False
    else:
        return True


def validate_email(user_email):
    student_email = Student.query.filter_by(email=user_email).first()
    teacher_email = Teacher.query.filter_by(email=user_email).first()
    if student_email or teacher_email:
        return False
    else:
        return True


def make_new_user(user_name, user_email, user_password, user_type):
    if user_type == "teacher":
        new_user = Teacher(user_name, user_email, user_password)
    else:
        new_user = Student(user_name, user_email, user_password)

    db.session.add(new_user)
    db.session.commit()


def user_authentication(user_name, user_password):
    student = Student.query.filter_by(user_name=user_name).first()
    teacher = Teacher.query.filter_by(user_name=user_name).first()

    if student and student.password == user_password:
        return "student"
    elif teacher and teacher.password == user_password:
        return "teacher"
    elif user_name == "admin" and user_password == "admin":
        return "admin"
    else:
        return "none"



