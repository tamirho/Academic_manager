import os
from werkzeug.utils import secure_filename
import secrets
from academic_manager.extensions import db
from academic_manager.models import Student, Course, Teacher, Enrollment, Task, File
from flask import current_app


def create_new_course(course_name, teacher_id):
    new_course = Course(course_name, teacher_id)
    db.session.add(new_course)
    db.session.commit()


def create_new_task(title, content, file_name, course_id, teacher_id):
    task = Task(title, content, course_id, teacher_id)
    db.session.add(task)
    db.session.commit()

    if file_name:
        create_new_file(file_name, task.id)


def create_new_file(file_name, task_id):
    new_file = File(file_name, task_id)
    db.session.add(new_file)
    db.session.commit()


def save_file(form_file, new_file_name, course_id):
    course = Course.query.get_or_404(course_id)
    directory = course.create_directory()
    if not directory:
        return

    # Define file name
    current_file_name, file_ext = os.path.splitext(form_file.filename)
    if new_file_name != "":
        filename = secure_filename(new_file_name)
    elif current_file_name:
        filename = secure_filename(current_file_name)
    else:
        filename = secrets.token_hex(8)

    filename = same_file_name(directory, filename, file_ext)

    form_file.save(directory + "/" + filename)
    return filename


def same_file_name(file_dir, filename, file_ext):
    path = os.path.join(file_dir, filename + file_ext)
    i = 0
    while os.path.isfile(path):
        i += 1
        new_copy = f"{filename}({i}){file_ext}"
        path = os.path.join(file_dir, new_copy)

    return f"{filename}{file_ext}" if i == 0 else f"{filename}({i}){file_ext}"

