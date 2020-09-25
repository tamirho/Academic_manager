from flask import redirect, url_for, render_template, request, session, flash, Blueprint
from academic_manager import db
from academic_manager.models import Course, Enrollment
from academic_manager.main.utilities import *

courses = Blueprint('courses', __name__, template_folder="templates", url_prefix="/courses")


@courses.route("/<int:course_id>/delete_course/")
def delete_course(course_id):
    course_to_del = Course.query.get(course_id)

    if "type" in session and course_to_del:
        course_name = course_to_del.course_name
        if course_to_del.lecturer.user_name == session["user_name"]:
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
