from academic_manager.models import Student, Enrollment, Course
from academic_manager import db


def make_new_enrollment(current_student, current_course):
    new_enroll = Enrollment(current_course.id, current_student.id)
    db.session.add(new_enroll)
    db.session.commit()


def get_best_student(course_id=0):
    if course_id:
        enrollment_list = Enrollment.query.filter_by(course_id=course_id)
        best_grade_enrollment = max(enrollment_list, key=lambda x: x.grade)
        return best_grade_enrollment.student
    else:
        student_list = Student.query.all()
        return max(student_list, key=lambda x: x.get_avg_grade())
