from flask import redirect, url_for, render_template, request, session, flash, Blueprint
from flask_login import current_user
from academic_manager.extensions import db, restricted
from academic_manager.models import Teacher, Course, Enrollment
from academic_manager.main.utilities import *

teachers = Blueprint('teachers', __name__, template_folder="templates", url_prefix="/teachers")


@teachers.route("/")
def teacher():
    return redirect(url_for("main.home"))


@teachers.route("/manage_courses/")
@restricted(role=["teacher"])
def manage_courses_teacher():
    return render_template("teacher_courses.html", teacher=current_user)


@teachers.route("/watch/<int:user_id>")
@restricted(role=["admin"])
def watch_teacher(user_id):
    teacher_profile = Teacher.query.filter_by(id=user_id).first_or_404()
    image_file = url_for('static', filename='profile_pics/' + teacher_profile.profile_img)
    return render_template("watch_teacher.html", teacher=teacher_profile, image_file=image_file)

