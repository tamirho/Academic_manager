from flask import redirect, url_for, render_template, request, session, flash, Blueprint
from academic_manager.extensions import db
from academic_manager.models import Course, Enrollment, Teacher, Student, Task
from academic_manager.main.utilities import *
from academic_manager.courses.utilities import *
from academic_manager.students.utilities import *

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
        if course_to_del.lecturer.user_name == session["user_name"] or session["type"] == "admin":
            course_name = course_to_del.course_name
            course_to_del.delete_from_db()
            flash(f"{course_name} has been deleted", "success")
            return redirect(request.referrer)

    flash("Page not found!", "warning")
    return redirect(url_for("main.home"))


@courses.route("/<int:course_id>/update_grades/", methods=['POST', 'GET'])
def update_grades(course_id):
    if request.method == "POST":
        course_to_view = Course.query.get(course_id)
        teacher = Teacher.query.get(course_to_view.teacher_id)
        if "type" in session and "user_name" in session and course_to_view:
            if session["user_name"] == teacher.user_name or session["type"] == "admin":
                for enroll in course_to_view.enrollment:
                    new_grade = request.form[enroll.student.user_name]
                    if new_grade:
                        enroll.grade = new_grade
                db.session.commit()
                return redirect(request.referrer)

    flash("Page not found!", "warning")
    return redirect(url_for("main.home"))


@courses.route("/<int:course_id>/add_task/", methods=['POST', 'GET'])
def add_task(course_id):
    if request.method == "POST":
        course_to_add = Course.query.get(course_id)
        teacher = course_to_add.lecturer
        if "type" in session and "user_name" in session and course_to_add and teacher:
            if session["user_name"] == teacher.user_name or session["type"] == "admin":
                title = request.form["title"]
                content = request.form["content"]
                make_new_task(title, content, course_to_add.id)
                flash(f"A new Task was added to {course_to_add.course_name} course ", "success")
                return redirect(url_for('courses.course_dashboard_teacher', course_id=course_to_add.id))

    flash("Error!", "danger")
    return redirect(url_for("main.home"))


@courses.route("/<int:task_id>/delete_task/", methods=['POST', 'GET'])
def delete_task(task_id):
    task_to_del = Task.query.get(task_id)
    teacher = task_to_del.course.lecturer
    if "type" in session and "user_name" in session and task_to_del and teacher:
        if session["user_name"] == teacher.user_name or session["type"] == "admin":
            title = task_to_del.title
            course = task_to_del.course
            task_to_del.delete_from_db()
            flash(f"Task '{title}' was successfully deleted from {course.course_name}", "success")
            return redirect(request.referrer)

    flash("Error!", "danger")
    return redirect(url_for("main.home"))


@courses.route("/<int:task_id>/update_task/", methods=['POST', 'GET'])
def update_task(task_id):
    task_to_update = Task.query.get(task_id)
    course = task_to_update.course
    teacher = course.lecturer
    if "type" in session and "user_name" in session and task_to_update and teacher:
        if session["user_name"] == teacher.user_name or session["type"] == "admin":
            if request.method == "POST":
                old_title = task_to_update.title
                task_to_update.update(request.form["title"], request.form["content"])
                flash(f"Task '{old_title}' in {task_to_update.course.course_name} has been successfully updated ",
                      "success")
                return redirect(url_for('courses.course_dashboard_teacher', course_id=course.id))
            else:
                return render_template('update_task.html', course=course, task=task_to_update)
    flash("Error!", "danger")
    return redirect(url_for("main.home"))


@courses.route("/<int:course_id>/course_control/", methods=['POST', 'GET'])
def course_dashboard_teacher(course_id):
    if request.method == "POST":
        pass  # todo edith later
    else:
        course_to_view = Course.query.get(course_id)
        tasks = Task.query.filter_by(course_id=course_id).order_by(Task.date_posted.desc()).all()
        best_student = get_best_student(course_id)
        if "type" in session and "user_name" in session and course_to_view:
            if session["user_name"] == course_to_view.lecturer.user_name or session["type"] == "admin":
                return render_template("course_dashboard_teacher.html", course=course_to_view, tasks=tasks,
                                       best_student=best_student)
    flash("Page not found!", "warning")
    return redirect(url_for("main.home"))


@courses.route("/<int:course_id>/dashboard/<int:student_id>", methods=['POST', 'GET'])
def course_dashboard_student(course_id, student_id):
    if request.method == "POST":
        pass  # todo edith later
    else:
        course_to_view = Course.query.get(course_id)
        tasks = Task.query.filter_by(course_id=course_id).order_by(Task.date_posted.desc()).all()
        best_student = get_best_student(course_id)
        student = Student.query.get(student_id)

        if "user_name" in session and course_to_view and student:
            if student.user_name == session["user_name"]:
                return render_template("course_dashboard_student.html", course=course_to_view,
                                       tasks=tasks, best_student=best_student)

    flash("Page not found!", "warning")
    return redirect(url_for("main.home"))


"""
# todo delete after use it
@courses.route("/<int:course_id>/view_course/")
def course_tasks(course_id):
    course_to_view = Course.query.get(course_id)
    tasks = Task.query.filter_by(course_id=course_id).order_by(Task.date_posted.desc()).all()
    teacher = Teacher.query.get(course_to_view.teacher_id)
    return render_template("course_tasks.html", course=course_to_view, tasks=tasks, teacher=teacher)


#  todo delete courses.course_tasks template
#  todo delete courses.course_grades template

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
                return redirect(url_for('courses.course_tasks', course_id=course_to_add.id))
            else:
                return render_template("update_task.html", course=course_to_add)

    flash("Page not found!", "warning")
    return redirect(url_for("main.home"))
    
    
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
                return redirect(request.referrer)
            else:
                return render_template("course_grades.html", course=course_to_view)

    flash("Page not found!", "warning")
    return redirect(url_for("main.home"))

"""
