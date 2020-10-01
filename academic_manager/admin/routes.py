from flask import redirect, url_for, render_template, request, session, flash, Blueprint
from academic_manager import db
from academic_manager.main.form_validation import *


admin = Blueprint('admin', __name__, template_folder="templates", url_prefix="/admin")


@admin.route("/", methods=['POST', 'GET'])
def admin_panel():
    student_list = Student.query.all()
    teacher_list = Teacher.query.all()
    courses_list = Course.query.all()
    return render_template("admin.html", student_list=student_list, teacher_list=teacher_list,
                           courses_list=courses_list)


@admin.route("/admin_students/")
def admin_students():
    student_list = Student.query.all()
    return render_template("admin_students.html", student_list=student_list)


@admin.route("/admin_teachers/")
def admin_teachers():
    teacher_list = Teacher.query.all()
    return render_template("admin_teachers.html", teacher_list=teacher_list)


@admin.route("/admin_courses/")
def admin_courses():
    courses_list = Course.query.all()
    return render_template("admin_courses.html", courses_list=courses_list)


@admin.route("/teacher_approval/<string:action>/<int:teacher_id>/")
def teacher_approval(teacher_id, action):
    current_teacher = Teacher.query.get(teacher_id)
    if "type" in session and current_teacher:
        if session["type"] == "admin":
            if action == "approve":
                current_teacher.approved = True
                flash(f"{current_teacher.user_name} has been approved", "success")
            elif action == "disapprove":
                current_teacher.approved = False
                flash(f"{current_teacher.user_name} has been disapproved", "warning")
            db.session.commit()
            return redirect(request.referrer)

    flash("Page not found!", "warning")
    return redirect(url_for("main.home"))


@admin.route("/search=?/", methods=['POST'])
def admin_search_panel():
    # todo can add smarter filters to search in db
    if request.method == "POST":
        value = request.form["search"]
        student = Student.query.filter_by(user_name=value).first()
        teacher = Teacher.query.filter_by(user_name=value).first()
        course = Course.query.filter_by(course_name=value).first()

        if student:
            return redirect(url_for('students.watch_student', student_id=student.id))
        elif teacher:
            return redirect(url_for('teachers.watch_teacher', teacher_id=teacher.id))
        elif course:
            return redirect(url_for('courses.view_course', course_id=course.id))
            # todo change this url after build the view course page

        flash("There is no such value!", "warning")
        return redirect(request.referrer)
