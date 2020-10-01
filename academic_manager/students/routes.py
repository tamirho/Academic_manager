from flask import redirect, url_for, render_template, request, session, flash, Blueprint
from academic_manager import db
from academic_manager.models import Student, Enrollment, Course
from academic_manager.main.utilities import *
from academic_manager.students.utilities import *

students = Blueprint('students', __name__, template_folder="templates", url_prefix="/students")


@students.route("/")
def student():
    student_profile = Student.query.filter_by(user_name=session["user_name"]).first()
    if "user_name" in session and student_profile:
        if session["user_name"] == student_profile.user_name:
            return render_template("student_profile.html", student=student_profile)

    flash("Page not found!", "warning")
    return redirect(url_for("main.home"))


@students.route("/<int:student_id>/update_student/", methods=['POST', 'GET'])
def update_student(student_id):
    student_to_update = Student.query.get(student_id)
    if "type" in session and student_to_update:
        if request.method == "POST":
            new_user_name = request.form["user_name"]
            new_email = request.form["user_email"]
            if student_to_update.user_name == session["user_name"]:
                messages = update_user_profile(student_to_update, new_user_name, new_email)
                session["user_name"] = student_to_update.user_name
                if not messages:
                    flash("Your details have been updated", "success")
                    return redirect(url_for("students.student"))
            elif session["type"] == "admin":
                messages = update_user_profile(student_to_update, new_user_name, new_email)
                if not messages:
                    flash(f"{student_to_update.user_name} details updated", "success")
                    return redirect(url_for("admin.admin_students"))
            else:
                flash("Page not found!", "warning")
                return redirect(url_for("main.home"))
            for msg in messages:
                flash(msg, "warning")
            return render_template("update_user_profile.html", user=student_to_update)
        elif student_to_update.user_name == session["user_name"] or session["type"] == "admin":
            return render_template("update_user_profile.html", user=student_to_update)

    flash("Page not found!", "warning")
    return redirect(url_for("main.home"))


@students.route("/<int:student_id>/change_password/", methods=['POST', 'GET'])
def change_student_password(student_id):
    student_to_update = Student.query.get(student_id)

    if "type" in session and student_to_update:
        if session["user_name"] == student_to_update.user_name:
            if request.method == "POST":
                old_pass = request.form["old_password"]
                new_pass = request.form["new_password"]
                pass_confirmation = request.form["password_confirmation"]

                messages = change_user_password(student_to_update, old_pass, new_pass, pass_confirmation)
                if not messages:
                    flash("Your password has been updated", "success")
                    return redirect(url_for("students.student"))
                else:
                    flash(messages[0], "warning")
                    return render_template("change_user_password.html")
            else:
                return render_template("change_user_password.html")

    flash("Page not found!", "warning")
    return redirect(url_for("main.home"))


@students.route("/<int:student_id>/delete_student/")
def delete_student(student_id):
    student_to_del = Student.query.get(student_id)

    if "type" in session and student_to_del:
        if student_to_del.user_name == session["user_name"]:
            Enrollment.query.filter(Enrollment.student_id == student_to_del.id).delete()
            db.session.delete(student_to_del)
            db.session.commit()
            flash("Your account has been deleted", "success")
            clear_user_info_from_session()  # todo check if session.clear() is better for me?
            return redirect(url_for("main.home"))
        elif session["type"] == "admin":
            flash(f"{student_to_del.user_name} has been deleted", "success")
            Enrollment.query.filter(Enrollment.student_id == student_to_del.id).delete()
            db.session.delete(student_to_del)
            db.session.commit()
            return redirect(url_for("admin.admin_panel"))

    flash("Page not found!", "warning")
    return redirect(url_for("main.home"))


@students.route("/manage_courses/")
def manage_courses_student():
    student_profile = Student.query.filter_by(user_name=session["user_name"]).first()
    if "user_name" in session and student_profile:
        if session["user_name"] == student_profile.user_name:
            return render_template("student_courses.html", student=student_profile)

    flash("Page not found!", "warning")
    return redirect(url_for("main.home"))


@students.route("/new_enrollment/", methods=['POST', 'GET'])
def new_enrollment():
    student_profile = Student.query.filter_by(user_name=session["user_name"]).first()
    current_courses_id_lst = student_profile.get_courses_id_lst()
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


@students.route("/remove_enrollment/<int:student_id>/<int:enrollment_id>")
def remove_enrollment(student_id, enrollment_id):
    enroll_to_del = Enrollment.query.get(enrollment_id)
    current_student = Student.query.get(student_id)
    current_course = enroll_to_del.course
    if "type" in session and enroll_to_del:
        if session["type"] == "student" and current_student.user_name == session["user_name"]:
            db.session.delete(enroll_to_del)
            db.session.commit()
            flash(f"{current_student.user_name} has been removed from {current_course.course_name}", "success")
            return redirect(url_for("students.manage_courses"))
        elif session["type"] == "admin" or \
                (session["type"] == "teacher" and current_course.lecturer.user_name == session["user_name"]):
            db.session.delete(enroll_to_del)
            db.session.commit()
            flash(f"{current_student.user_name} has been removed from {current_course.course_name}", "success")
            return redirect(request.referrer)

    flash("Page not found!", "warning")
    return redirect(url_for("main.home"))


@students.route("/watch/<int:student_id>")
def watch_student(student_id):
    if "type" in session:
        if session["type"] == "admin" or session["type"] == "teacher":
            student_profile = Student.query.filter_by(id=student_id).first()
            return render_template("watch_student.html", student=student_profile)

    flash("Page not found!", "warning")
    return redirect(url_for("main.home"))
