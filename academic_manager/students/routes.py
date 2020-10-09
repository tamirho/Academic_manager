from flask import redirect, url_for, render_template, request, session, flash, Blueprint, abort
from flask_login import current_user, login_required
from academic_manager.extensions import db, restricted
from academic_manager.models import Student, Enrollment, Course
from academic_manager.main.utilities import *
from academic_manager.students.utilities import *

students = Blueprint('students', __name__, template_folder="templates", url_prefix="/students")


@students.route("/")
def student():
    return redirect(url_for("main.home"))


@students.route("/<int:student_id>/delete_student/")
def delete_student(student_id):
    student_to_del = Student.query.get(student_id)

    if "type" in session and student_to_del:
        if student_to_del.user_name == session["user_name"]:
            student_to_del.delete_from_db()
            flash("Your account has been deleted", "success")
            return redirect(url_for("main.home"))
        elif session["type"] == "admin":
            flash(f"{student_to_del.user_name} has been deleted", "success")
            student_to_del.delete_from_db()
            return redirect(url_for("admin.admin_students"))

    flash("Page not found!", "warning")
    return redirect(url_for("main.home"))


@students.route("/manage_courses/")
@restricted(role=["student"])
def manage_courses_student():
    return render_template("student_courses.html", student=current_user)


@students.route("/new_enrollment/", methods=['POST', 'GET'])
@restricted(role=["student"])
def new_enrollment():
    current_courses_id_lst = current_user.get_courses_id_lst()
    courses_to_enroll = [course for course in Course.query.all()
                         if course.id not in current_courses_id_lst]
    if request.method == "POST":
        course_name = request.form["course_name"]
        current_course = Course.query.filter_by(course_name=course_name).first()
        if current_course:
            if current_course.id not in current_courses_id_lst:
                make_new_enrollment(student_profile, current_course)
                flash(f"You have successfully enrolled for {course_name}", "success")
            else:
                flash(f"There was a problem registering, please try again later", "warning")
            return render_template("student_courses.html", student=student_profile)
        else:
            flash(f"Please choose course before you submit", "warning")
            return render_template("new_enrollment.html", student=student_profile, courses=courses_to_enroll)
    else:
        return render_template("new_enrollment.html", student=student_profile, courses=courses_to_enroll)


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


@students.route("/watch/<int:student_id>")
def watch_student(student_id):
    student_profile = Student.query.filter_by(id=student_id).first()
    return render_template("watch_student.html", student=student_profile)

