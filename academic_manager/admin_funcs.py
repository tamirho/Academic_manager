from academic_manager.models import Student, Teacher, Enrollment, Course
from academic_manager import db


def validate_course_name(course_name):
    course = Course.query.filter_by(course_name=course_name).first()
    if course:
        return False
    else:
        return True


def make_new_course_by_names(course_name, teacher_name):
    current_teacher = Teacher.query.filter_by(user_name=teacher_name).first()
    new_course = Course(course_name, current_teacher.id)
    db.session.add(new_course)
    db.session.commit()
