from academic_manager.models import Student, Enrollment, Course
from academic_manager import db


def make_new_enrollment(current_student, current_course):
    new_enroll = Enrollment(current_course.id, current_student.id)
    db.session.add(new_enroll)
    db.session.commit()

