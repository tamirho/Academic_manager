from flask import redirect, url_for, render_template, request, session, flash, Blueprint, abort
from academic_manager.extensions import db, restricted
from flask_login import current_user, login_required
from academic_manager.forms import AddCourseForm, AddTaskForm
from academic_manager.models import Course, Enrollment, Teacher, Student, Task
from academic_manager.main.utilities import *
from academic_manager.courses.utilities import *
from academic_manager.students.utilities import *

courses = Blueprint('courses', __name__, template_folder="templates", url_prefix="/courses")


@courses.route("/add_course/", methods=['POST', 'GET'])
@restricted(role=["admin", "teacher"])
def add_course():
    form = AddCourseForm()

    # create teachers list
    if current_user.is_admin:
        teachers_lst = [(teacher.id, teacher.full_name) for teacher in Teacher.query.all()]
        teachers_lst.insert(0, ('0', "Choose.."))
    else:
        teachers_lst = [(current_user.id, current_user.full_name)]

    if form.validate_on_submit():
        course_name = form.course.data
        teacher_id = form.teacher.data
        make_new_course(course_name, teacher_id)
        flash("The course is added to the list", "success")
        return redirect(url_for("courses.add_course"))
    else:
        form.teacher.choices = teachers_lst

    return render_template("add_course.html", form=form, lst=teachers_lst)


@courses.route("/<int:course_id>/delete_course/")
@restricted(role=["admin", "teacher"])
def delete_course(course_id):
    course_to_del = Course.query.get_or_404(course_id)

    # Prevents teachers who do not teach the course from deleting it
    if current_user.is_teacher and course_to_del.lecturer != current_user:
        abort(403)

    course_name = course_to_del.course_name
    course_to_del.delete_from_db()
    flash(f"{course_name} has been deleted", "success")
    return redirect(request.referrer)


# todo this
@courses.route("/<int:course_id>/update_grades/", methods=['POST', 'GET'])
@restricted(role=["admin", "teacher"])
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


# todo this
@courses.route("/<int:course_id>/add_task/", methods=['POST', 'GET'])
@restricted(role=["admin", "teacher"])
def add_task(course_id):
    form = AddTaskForm(request.form)
    course_to_add = Course.query.get_or_404(course_id)

    if form.validate_on_submit():

        # Files handling
        if form.file.data:  # todo this
            file = form.file.data
        else:
            file = None

        title = form.title.data
        content = form.content.data
        make_new_task(title, content, file, course_to_add.id)
        flash(f"A new Task was added to {course_to_add.course_name} course ", "success")

    return redirect(request.referrer)


@courses.route("/<int:task_id>/delete_task/", methods=['POST', 'GET'])
@restricted(role=["admin", "teacher"])
def delete_task(task_id):
    task_to_del = Task.query.get_or_404(task_id)
    teacher = task_to_del.course.lecturer

    # Prevents teachers who do not teach the course from deleting tasks
    if current_user.is_teacher and teacher != current_user:
        abort(403)

    title = task_to_del.title
    course = task_to_del.course
    task_to_del.delete_from_db()
    flash(f"Task '{title}' was successfully deleted from {course.course_name}", "success")
    return redirect(request.referrer)


# todo this
@courses.route("/<int:task_id>/update_task/", methods=['POST', 'GET'])
@restricted(role=["admin", "teacher"])
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


# todo this
@courses.route("/<int:course_id>/course_control/", methods=['POST', 'GET'])
@restricted(role=["admin", "teacher"])
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


# todo this
@courses.route("/<int:course_id>/dashboard/<int:user_id>", methods=['POST', 'GET'])
@restricted(role=["student"])
def course_dashboard_student(course_id, user_id):
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

