from flask import redirect, url_for, render_template, request, session, flash, Blueprint
from academic_manager import db
from academic_manager.models import Teacher, Course, Enrollment
from academic_manager.main.utilities import *

teachers = Blueprint('teachers', __name__, template_folder="templates", url_prefix="/teachers")


@teachers.route("/")
def teacher():
    teacher_profile = Teacher.query.filter_by(user_name=session["user_name"]).first()
    return render_template("teacher.html", teacher=teacher_profile)


@teachers.route("/<int:teacher_id>/delete_teacher/")
def delete_teacher(teacher_id):
    teacher_to_del = Teacher.query.get(teacher_id)

    if "type" in session and teacher_to_del:
        if teacher_to_del.user_name == session["user_name"]:
            Course.query.filter(Course.teacher_id == teacher_to_del.id).delete()
            db.session.delete(teacher_to_del)
            db.session.commit()
            flash("Your account has been deleted", "success")
            clear_user_info_from_session()  # todo check if session.clear() is better for me?
            return redirect(url_for("main.home"))
        elif session["type"] == "admin":
            flash(f"{teacher_to_del.user_name} has been deleted", "success")
            Course.query.filter(Course.teacher_id == teacher_to_del.id).delete()
            db.session.delete(teacher_to_del)
            db.session.commit()
            return redirect(url_for("admin.admin_panel"))

    flash("Page not found!", "warning")
    return redirect(url_for("main.home"))


@teachers.route("/delete_course/<int:course_id>")
def delete_course(course_id):
    course_to_del = Course.query.get(course_id)

    if "type" in session and course_to_del:
        course_name = course_to_del.course_name
        if course_to_del.lecturer == session["user_name"]:
            Enrollment.query.filter(Enrollment.course_id == course_to_del.id).delete()
            db.session.delete(course_to_del)
            db.session.commit()
            flash(f"{course_name} has been deleted", "success")
            return redirect(url_for("main.home"))  # todo find another page to redirect
        elif session["type"] == "admin":

            Enrollment.query.filter(Enrollment.course_id == course_to_del.id).delete()
            db.session.delete(course_to_del)
            db.session.commit()
            flash(f"{course_name} has been deleted", "success")
            return redirect(url_for("admin.admin_panel"))

    flash("Page not found!", "warning")
    return redirect(url_for("main.home"))


