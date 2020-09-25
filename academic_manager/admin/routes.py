from flask import redirect, url_for, render_template, request, session, flash, Blueprint
from academic_manager import db
from academic_manager.main.form_validation import *
from academic_manager.admin.admin_funcs import *


admin = Blueprint('admin', __name__, template_folder="templates", url_prefix="/admin")


@admin.route("/", methods=['POST', 'GET'])
def admin_panel():
    student_list = Student.query.all()
    teacher_list = Teacher.query.all()
    courses_list = Course.query.all()
    return render_template("admin.html", student_list=student_list, teacher_list=teacher_list,
                           courses_list=courses_list)


@admin.route("/add_course/", methods=['POST', 'GET'])
def add_course():
    if request.method == "POST":
        course_name = request.form["course_name"]
        teacher_name = request.form["teacher_name"]
        if validate_course_name(course_name):
            make_new_course_by_names(course_name, teacher_name)
            flash("The course is added to the list", "success")
            return redirect(url_for("admin.admin_panel"))
        else:
            flash("That Course name is invalid", "warning")
            return redirect(url_for("admin.add_course"))
    else:
        teacher_list = Teacher.query.all()
        return render_template("add_course.html", teacher_list=teacher_list)
