from flask import redirect, url_for, render_template, request, session, flash, Blueprint
from academic_manager import db
from academic_manager.models import Student, Enrollment
from academic_manager.main.utilities import *

students = Blueprint('students', __name__, template_folder="templates", url_prefix="/students")


@students.route("/")
def student():
    student_profile = Student.query.filter_by(user_name=session["user_name"]).first()
    return render_template("student.html", student=student_profile)


@students.route("/<int:student_id>/delete_student/")
def delete_student(student_id):
    student_to_del = Student.query.get(student_id)

    if session["type"] and student_to_del:
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



