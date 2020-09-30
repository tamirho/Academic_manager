from flask import redirect, url_for, render_template, request, session, flash, Blueprint

from academic_manager import db
from academic_manager.models import Course, Enrollment, Teacher, Student, Task
from academic_manager.main.utilities import *
from academic_manager.courses.utilities import *

courses = Blueprint('courses', __name__, template_folder="templates", url_prefix="/courses")


@courses.route("/add_course/", methods=['POST', 'GET'])
def add_course():
    if request.method == "POST":
        course_name = request.form["course_name"]
        teacher_name = request.form["teacher_name"]
        if validate_course_name(course_name):
            make_new_course_by_names(course_name, teacher_name)
            flash("The course is added to the list", "success")
            return redirect(url_for("courses.add_course"))
        else:
            flash("That Course name is invalid", "warning")
            return redirect(url_for("courses.add_course"))
    else:
        if "type" in session:
            if session["type"] == "admin":
                teacher_list = Teacher.query.all()
                return render_template("add_course.html", teacher_list=teacher_list)
            elif session["type"] == "teacher":
                current_teacher = Teacher.query.filter_by(user_name=session["user_name"]).first()
                return render_template("add_course.html", current_teacher=current_teacher)

        flash("Page not found!", "warning")
        return redirect(url_for("main.home"))


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


@courses.route("/<int:course_id>/view_course/")
def view_course(course_id):
    course_to_view = Course.query.get(course_id)
    tasks = Task.query.filter_by(course_id=course_id).order_by(Task.date_posted.desc()).all()
    teacher = Teacher.query.get(course_to_view.teacher_id)
    return render_template("course_tasks.html", course=course_to_view, tasks=tasks, teacher=teacher)


@courses.route("/<int:course_id>/update_grades/", methods=['POST', 'GET'])
def update_grades(course_id):
    course_to_view = Course.query.get(course_id)
    teacher = Teacher.query.get(course_to_view.teacher_id)
    if "type" in session and "user_name" in session and course_to_view:
        if session["user_name"] == teacher.user_name or session["type"] == "admin":
            if request.method == "POST":
                for enroll in course_to_view.enrollment:
                    new_grade = request.form[enroll.student.user_name]
                    if new_grade:
                        enroll.grade = new_grade
                db.session.commit()
                return render_template("course_grades.html", course=course_to_view)
            else:
                return render_template("course_grades.html", course=course_to_view)

    flash("Page not found!", "warning")
    return redirect(url_for("main.home"))


@courses.route("/<int:course_id>/add_task/", methods=['POST', 'GET'])
def add_task(course_id):
    course_to_add = Course.query.get(course_id)
    teacher = Teacher.query.get(course_to_add.teacher_id)
    if "type" in session and "user_name" in session and course_to_add and teacher:
        if session["user_name"] == teacher.user_name or session["type"] == "admin":
            if request.method == "POST":
                title = request.form["title"]
                content = request.form["content"]
                make_new_task(title, content, course_to_add.id)
                flash(f"A new Task was added to {course_to_add.course_name} course ", "success")
                return render_template("add_task.html", course=course_to_add)
            else:
                return render_template("add_task.html", course=course_to_add)

    flash("Page not found!", "warning")
    return redirect(url_for("main.home"))
