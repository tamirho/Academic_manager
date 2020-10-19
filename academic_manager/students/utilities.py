from academic_manager.models import Student, Enrollment, Course
from academic_manager.extensions import db


def make_new_enrollment(student_id, course_id):
    new_enroll = Enrollment(course_id, student_id)
    db.session.add(new_enroll)
    db.session.commit()


def get_best_student(course_id=0):
    if course_id:
        try:
            enrollment_list = Enrollment.query.filter_by(course_id=course_id)
            best_grade_enrollment = max(enrollment_list, key=lambda x: x.grade)
            return best_grade_enrollment.student
        except:
            return None
    else:
        try:
            student_list = Student.query.all()
            return max(student_list, key=lambda x: x.avg())
        except:
            return None

