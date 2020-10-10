from flask import redirect, url_for, render_template, request, session, flash, Blueprint, abort
from flask_login import current_user, login_required
from academic_manager.extensions import db, restricted
from academic_manager.forms import NewEnrollmentForm
from academic_manager.models import Student, Enrollment, Course
from academic_manager.main.utilities import *
from academic_manager.students.utilities import *

students = Blueprint('students', __name__, template_folder="templates", url_prefix="/students")


@students.route("/")
def student():
    return redirect(url_for("main.home"))


@students.route("/manage_courses/")
@restricted(role=["student"])
def manage_courses_student():
    return render_template("student_courses.html", student=current_user)


@students.route("/new_enrollment/", methods=['POST', 'GET'])
@restricted(role=["student"])
def new_enrollment():
    form = NewEnrollmentForm()

    # create courses to enroll list for the Select Field (choices)
    current_courses_id_lst = current_user.get_courses_id_lst()
    courses_to_enroll = [(course.id, course.course_name + " (" + course.lecturer.full_name + ")")
                         for course in Course.query.all()
                         if course.id not in current_courses_id_lst]
    courses_to_enroll.insert(0, ('0', "Choose Course:"))

    if request.method == "GET":
        form.enrollment.choices = courses_to_enroll
        return render_template("new_enrollment.html", form=form, courses=courses_to_enroll)

    if form.validate_on_submit():
        course_id = form.enrollment.data
        course = Course.query.get(course_id)
        make_new_enrollment(current_user.id, course_id)
        flash(f"You have successfully enrolled for {course.course_name} ", "success")

    return redirect(url_for('students.new_enrollment'))


@students.route("/remove_enrollment/<int:user_id>/<int:enrollment_id>")
@restricted(role=["admin", "teacher", "current_user"])
def remove_enrollment(user_id, enrollment_id):
    enroll_to_del = Enrollment.query.get(enrollment_id)
    current_student = Student.query.get(user_id)
    current_course = enroll_to_del.course
    if enroll_to_del:
        if current_user.is_teacher and current_course.lecturer != current_user:
            abort(403)
        else:
            enroll_to_del.delete_from_db()
            flash(f"{current_student.full_name} has been removed from {current_course.course_name}", "success")
            return redirect(request.referrer)


@students.route("/watch/<int:user_id>")
@restricted(role=["admin", "teacher"])
def watch_student(user_id):
    student_profile = Student.query.filter_by(id=user_id).first_or_404()
    return render_template("watch_student.html", student=student_profile)

