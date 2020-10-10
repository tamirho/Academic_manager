from academic_manager.models import Student, Teacher, Enrollment, Course
from academic_manager.extensions import db
from academic_manager.models import Student, Course, Teacher, Enrollment, Task


def make_new_course(course_name, teacher_id):
    new_course = Course(course_name, teacher_id)
    db.session.add(new_course)
    db.session.commit()


def make_new_task(title, content, file, course_id):
    task = Task(title, content, course_id)

    if file:
        task.file = file.read()

    db.session.add(task)
    db.session.commit()



