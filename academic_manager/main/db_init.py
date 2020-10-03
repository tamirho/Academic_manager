from academic_manager.models import Student, Teacher, Admin, Enrollment, Course, Task
from academic_manager import db
import random


def init_db():
    db.drop_all()
    db.create_all()

    admin_init()
    student_init()
    teacher_init()
    course_init()
    enrollment_init_auto()
    task_init()
    print("# - - - finish - - - #")


def admin_init():
    admin = Admin('admin', 'admin')
    db.session.add(admin)
    db.session.commit()
    print(Admin.query.all())


def student_init():
    student_list = [Student('Tamir', 'Tamir@gmail.com', '123'),
                    Student('Sapir', 'Sapir@gmail.com', '123'),
                    Student('Hadar', 'Hadar@gmail.com', '123'),
                    Student('Boten', 'tamir@gmail.com', '123'),
                    Student('Din', 'Boten@gmail.com', '123'),
                    Student('Shaked', 'Shaked@gmail.com', '123'),
                    Student('Roni', 'Roni@gmail.com', '123'),
                    Student('Gal', 'Gal@gmail.com', '123'),
                    Student('Dafna', 'Dafna@gmail.com', '123'),
                    Student('Matan', 'Matan@gmail.com', '123'),
                    Student('Daniel', 'Daniel@gmail.com', '123'),
                    Student('Roi', 'Roi@gmail.com', '123'),
                    Student('Eden', 'Eden@gmail.com', '123'),
                    Student('Aviva', 'Aviva@gmail.com', '123'),
                    Student('David', 'David@gmail.com', '123'),
                    Student('Yael', 'Yael@gmail.com', '123'),
                    Student('Adi', 'Adi@gmail.com', '123'),
                    Student('Sharon', 'Sharon@gmail.com', '123'),
                    Student('Danit', 'Danit@gmail.com', '123'),
                    Student('Ronit', 'Ronit@gmail.com', '123')]

    for student in student_list:
        db.session.add(student)
    db.session.commit()
    print(Student.query.all())


def teacher_init():
    teacher_list = [Teacher('Mali', 'Mali@gmail.com', '123'),
                    Teacher('Zohar', 'Zohar@gmail.com', '123'),
                    Teacher('Ofir', 'Ofir@gmail.com', '123'),
                    Teacher('Almog', 'Almog@gmail.com', '123'),
                    Teacher('Peleg', 'Peleg@gmail.com', '123'),
                    Teacher('Boaz', 'Boaz@gmail.com', '123'),
                    Teacher('Iris', 'Iris@gmail.com', '123')]

    for teacher in teacher_list:
        db.session.add(teacher)
    db.session.commit()
    print(Teacher.query.all())


def course_init():
    course_list = [Course('algebra 1', 1),
                   Course('english 1', 1),
                   Course('spanish 1', 2),
                   Course('calculus 1', 2),
                   Course('progreming 1', 3),
                   Course('algebra 2', 3),
                   Course('english 2', 4),
                   Course('spanish 2', 4),
                   Course('calculus 2', 5),
                   Course('progreming 2', 5),
                   Course('sports', 6),
                   Course('deep learning', 7),
                   Course('c++', 7),
                   Course('trx', 6)]

    for course in course_list:
        db.session.add(course)
    db.session.commit()
    print(Course.query.all())


def enrollment_init():
    enrollment_list = [Enrollment(1, 1),
                       Enrollment(2, 2),
                       Enrollment(3, 3),
                       Enrollment(4, 4),
                       Enrollment(5, 5),
                       Enrollment(6, 6),
                       Enrollment(7, 7),
                       Enrollment(8, 8),
                       Enrollment(9, 9),
                       Enrollment(10, 10),
                       Enrollment(11, 11),
                       Enrollment(12, 12),
                       Enrollment(13, 13),
                       Enrollment(14, 14),
                       Enrollment(1, 15),
                       Enrollment(2, 16),
                       Enrollment(3, 17),
                       Enrollment(4, 18),
                       Enrollment(5, 19),
                       Enrollment(6, 20)]

    for enrollment in enrollment_list:
        db.session.add(enrollment)
    db.session.commit()
    print(Enrollment.query.all())


def enrollment_init_auto():
    stu = 1
    for i in range(0, 10):
        for course in range(1, 15):
            enrol1 = Enrollment(course, stu)
            enrol1.grade = random.randint(45, 100)
            db.session.add(enrol1)
            if stu == 20:
                stu = 1
            else:
                stu += 1
    db.session.commit()
    print(Enrollment.query.all())


def task_init():
    for course in range(1, 15):
        task1 = Task('Task 1', 'hello students this is my first task', course)
        task2 = Task('Homework', 'homework task: do questions 1,2,3,4,5,6 from the notebook', course)
        task3 = Task('Task 2', 'hello students this is my seconed task', course)
        task4 = Task('Homework', 'homework task: do questions 7,8,9 from the notebook', course)
        db.session.add(task1)
        db.session.add(task2)
        db.session.add(task3)
        db.session.add(task4)
        db.session.commit()

    print(Task.query.all())
