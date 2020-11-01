from flask import redirect, url_for, render_template, request, session, flash, Blueprint, abort
from academic_manager.extensions import restricted
from flask_login import current_user, login_required
from academic_manager.courses.forms import CourseForm, TaskForm
from academic_manager.main.utilities import *
from academic_manager.courses.utilities import *
from academic_manager.students.utilities import *


courses = Blueprint('courses', __name__, template_folder="templates", url_prefix="/courses")


@courses.route("/add-course/", methods=['POST', 'GET'])
@restricted(role=["admin", "teacher"])
def add_course():
    form = CourseForm()

    # create teachers list
    if current_user.is_admin:
        teachers_lst = [(teacher.id, teacher.full_name) for teacher in Teacher.query.all()]
        teachers_lst.insert(0, ('0', "Choose.."))
    else:
        teachers_lst = [(current_user.id, current_user.full_name)]

    if form.validate_on_submit():
        course_name = form.course.data
        teacher_id = form.teacher.data
        create_new_course(course_name, teacher_id)
        flash(f"The course '{course_name}' has been added", "success")
        return redirect(url_for("courses.add_course"))
    else:
        form.teacher.choices = teachers_lst

    return render_template("add_course.html", form=form, lst=teachers_lst)


@courses.route("/delete-course/<int:course_id>/")
@restricted(role=["admin", "teacher"])
def delete_course(course_id):
    current_course = Course.query.get_or_404(course_id)

    # Prevents teachers who do not teach the course from deleting it
    if current_user.is_teacher and current_course.lecturer != current_user:
        abort(403)

    course_name = current_course.course_name
    current_course.delete_from_db()
    flash(f"{course_name} has been deleted", "success")
    return redirect(request.referrer)


@courses.route("/dashboard/<int:course_id>/")
@courses.route("/dashboard/<int:course_id>/main/")
@login_required
def course_dashboard(course_id):
    course = Course.query.get_or_404(course_id)
    last_task = Task.query.filter_by(course_id=course_id).order_by(Task.date_posted.desc()).first()
    best_student = get_best_student(course_id)
    return render_template('dashboard_main.html', course=course, task=last_task, best_student=best_student)


@courses.route("/dashboard/<int:course_id>/add-task/", methods=['POST', 'GET'])
@restricted(role=["admin", "teacher"])
def dashboard_add_tasks(course_id):
    form = TaskForm()
    current_course = Course.query.get_or_404(course_id)
    teacher = current_course.lecturer

    # Prevents teachers who do not teach the course from add tasks
    if current_user.is_teacher and teacher != current_user:
        abort(403)

    if form.validate_on_submit():

        # Files handling
        if form.file.data:
            new_file_name = form.file_name.data if form.file_name.data else ""
            # Save the file in uploads folder
            file_name = save_file(form.file.data, new_file_name, course_id)
        else:
            file_name = None

        create_new_task(title=form.title.data, content=form.content.data, file_name=file_name,
                        course_id=current_course.id, teacher_id=teacher.id)

        flash(f"A new Task was added to {current_course.course_name} course ", "success")
        return redirect(url_for("courses.dashboard_view_tasks", course_id=course_id))

    return render_template('dashboard_task.html', course=current_course, form=form,
                           page_name="New Task")


@courses.route("/dashboard/delete_task/<int:task_id>/", methods=['POST', 'GET'])
@restricted(role=["admin", "teacher"])
def dashboard_delete_task(task_id):
    current_task = Task.query.get_or_404(task_id)
    teacher = current_task.course.lecturer

    # Prevents teachers who do not teach the course from deleting tasks
    if current_user.is_teacher and teacher != current_user:
        abort(403)

    title = current_task.title
    course = current_task.course
    current_task.delete_from_db()
    flash(f"Task '{title}' was successfully deleted from {course.course_name}", "success")
    return redirect(url_for('courses.dashboard_view_tasks', course_id=course.id))


@courses.route("/dashboard/<int:course_id>/update-task/<int:task_id>/", methods=['POST', 'GET'])
@restricted(role=["admin", "teacher"])
def dashboard_edit_task(course_id, task_id):
    form = TaskForm()
    current_task = Task.query.get_or_404(task_id)
    current_course = Course.query.get_or_404(course_id)
    teacher = current_course.lecturer

    # Prevents teachers who do not teach the course from edit tasks
    if current_user.is_teacher and teacher != current_user:
        abort(403)

    if form.validate_on_submit():

        # Files handling
        if form.file.data:
            new_file_name = form.file_name.data if form.file_name.data else ""
            # Save the file in uploads folder
            file_name = save_file(form.file.data, new_file_name, course_id)
            create_new_file(file_name, task_id)

        current_task.title = form.title.data
        current_task.content = form.content.data
        current_task.add_update_time()
        db.session.commit()
        flash(f"Your Task has been update! ", "success")
        return redirect(url_for("courses.dashboard_view_tasks", course_id=course_id))

    elif request.method == "GET":
        form.title.data = current_task.title
        form.content.data = current_task.content

    return render_template('dashboard_task.html', course=current_course, form=form,
                           page_name="Edit Task")


@courses.route("/dashboard/<int:course_id>/view-tasks/")
@login_required
def dashboard_view_tasks(course_id):
    current_course = Course.query.get_or_404(course_id)
    tasks = Task.query.filter_by(course_id=course_id).order_by(Task.date_posted.desc()).all()
    return render_template("dashboard_view_tasks.html", course=current_course, tasks=tasks)


@courses.route("/dashboard/<int:course_id>/view-task/<int:task_id>")
@login_required
def dashboard_single_task(course_id, task_id):
    current_task = Task.query.get_or_404(task_id)
    current_course = Course.query.get_or_404(course_id)
    return render_template("dashboard_single_task.html", course=current_course, task=current_task)


@courses.route("/dashboard/<int:course_id>/participants")
@login_required
def dashboard_participants(course_id):
    current_course = Course.query.get_or_404(course_id)
    return render_template("dashboard_participants.html", course=current_course)


@courses.route("/dashboard/<int:course_id>/grades/", methods=['POST', 'GET'])
@restricted(role=["admin", "teacher"])
def dashboard_update_grades(course_id):
    current_course = Course.query.get_or_404(course_id)
    teacher = Teacher.query.get(current_course.teacher_id)

    # Prevents teachers who do not teach the course from edit grades
    if current_user.is_teacher and teacher != current_user:
        abort(403)

    if request.method == "POST":
        for enroll in current_course.enrollment:
            new_grade = request.form[str(enroll.id)]
            if new_grade:
                enroll.grade = new_grade
        db.session.commit()
        return redirect(request.referrer)

    return render_template("dashboard_update_grades.html", course=current_course)


@courses.route("/dashboard/<int:course_id>/remove-file/<int:file_id>/")
@restricted(role=["admin", "teacher"])
def remove_file(course_id, file_id):
    current_course = Course.query.get_or_404(course_id)
    file = File.query.get_or_404(file_id)

    # Prevents teachers who do not teach the course from remove files
    if current_user.is_teacher and current_course.lecturer != current_user:
        abort(403)

    file_name = file.name
    file.delete_from_db()
    flash(f"{file_name} has been deleted", "success")
    return redirect(request.referrer)
