from flask import redirect, url_for, render_template, request, session, flash, Blueprint
from academic_manager import db
from academic_manager.models import Teacher, Course, Enrollment
from academic_manager.main.utilities import *

teachers = Blueprint('teachers', __name__, template_folder="templates", url_prefix="/teachers")


@teachers.route("/")
def teacher():
    teacher_profile = Teacher.query.filter_by(user_name=session["user_name"]).first()
    return render_template("teacher_profile.html", teacher=teacher_profile)


@teachers.route("/<int:teacher_id>/update_teacher/", methods=['POST', 'GET'])
def update_teacher(teacher_id):
    teacher_to_update = Teacher.query.get(teacher_id)
    if "type" in session and teacher_to_update:
        if request.method == "POST":
            new_user_name = request.form["user_name"]
            new_email = request.form["user_email"]
            if teacher_to_update.user_name == session["user_name"]:
                messages = update_user_profile(teacher_to_update, new_user_name, new_email)
                session["user_name"] = teacher_to_update.user_name
                if not messages:
                    flash("Your details have been updated", "success")
                    return redirect(url_for("teachers.teacher"))
            elif session["type"] == "admin":
                messages = update_user_profile(teacher_to_update, new_user_name, new_email)
                if not messages:
                    flash(f"{teacher_to_update.user_name} details updated", "success")
                    return redirect(url_for("admin.admin_teachers"))
            else:
                flash("Page not found!", "warning")
                return redirect(url_for("main.home"))
            for msg in messages:
                flash(msg, "warning")
            return render_template("update_user_profile.html", teacher=teacher_to_update)
        elif teacher_to_update.user_name == session["user_name"] or session["type"] == "admin":
            return render_template("update_user_profile.html", teacher=teacher_to_update)


@teachers.route("/<int:teacher_id>/change_password/", methods=['POST', 'GET'])
def change_teacher_password(teacher_id):
    teacher_to_update = Teacher.query.get(teacher_id)

    if "type" in session and teacher_to_update:
        if session["user_name"] == teacher_to_update.user_name:
            if request.method == "POST":
                old_pass = request.form["old_password"]
                new_pass = request.form["new_password"]
                pass_confirmation = request.form["password_confirmation"]

                messages = change_user_password(teacher_to_update, old_pass, new_pass, pass_confirmation)
                if not messages:
                    flash("Your password has been updated", "success")
                    return redirect(url_for("teachers.teacher"))
                else:
                    flash(messages[0], "warning")
                    return render_template("change_user_password.html")
            else:
                return render_template("change_user_password.html")
    flash("Page not found!", "warning")
    return redirect(url_for("main.home"))


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





