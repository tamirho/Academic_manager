from academic_manager.models import Student, Teacher, Admin, Enrollment, Course, Task
from academic_manager.extensions import db, bcrypt
import random


def init_db():
    db.drop_all()
    db.create_all()

    admin_init()
    teacher_init()
    student_init()

    course_init()
    enrollment_init()
    task_init()
    print("# - - - finish - - - #")


def password():
    return bcrypt.generate_password_hash('123').decode('utf-8')


def admin_init():
    pw = password()
    admin = Admin('Admin@gmail.com', 'Admin', 'Admin', pw, 'Male')
    db.session.add(admin)
    db.session.commit()
    print(Admin.query.all())


def student_init():
    pw = password()
    student_list1 = [Student('Tamir@gmail.com', 'Tamir', 'Houri', pw, 'Male'),
                     Student('Hadar@gmail.com', 'Hadar', 'Perets', pw, 'Female'),
                     Student('Sapir@gmail.com', 'Sapir', 'Houri', pw, 'Female'),
                     Student('Shaked@gmail.com', 'Shaked', 'Houri', pw, 'Female'),
                     Student('Boten@gmail.com', 'Boten', 'Houri', pw, 'Female'),
                     Student('Din@gmail.com', 'Din', 'Smith', pw, 'Male'),
                     Student('Roni@gmail.com', 'Roni', 'Smith', pw, 'Male'),
                     Student('Gal@gmail.com', 'Gal', 'Smith', pw, 'Male'),
                     Student('Oliver@gmail.com', 'Oliver', 'Smith', pw, 'Male'),
                     Student('Jack@gmail.com', 'Jack', 'Murphy', pw, 'Male'),
                     Student('Harry@gmail.com', 'Harry', 'Murphy', pw, 'Male'),
                     Student('Thomas@gmail.com', 'Thomas', 'Murphy', pw, 'Male'),
                     Student('George@gmail.com', 'George', 'Murphy', pw, 'Male'),
                     Student('Amelia@gmail.com', 'Amelia', 'Jones', pw, 'Female'),
                     Student('Isabella@gmail.com', 'Isabella', 'Jones', pw, 'Female'),
                     Student('Mary@gmail.com', 'Mary', 'Jones', pw, 'Female'),
                     Student('Jessica@gmail.com', 'Jessica', 'Jones', pw, 'Female'),
                     Student('Sarah@gmail.com', 'Sarah', 'Williams', pw, 'Female'),
                     Student('Yael@gmail.com', 'Yael', 'Williams', pw, 'Female'),
                     Student('Adi@gmail.com', 'Adi', 'Williams', pw, 'Female'),
                     Student('Matan@gmail.com', 'Matan', 'Williams', pw, 'Male'),
                     Student('Jake@gmail.com', 'Jake', 'Johnson', pw, 'Male'),
                     Student('Jacob@gmail.com', 'Jacob', 'Johnson', pw, 'Male'),
                     Student('Ethan@gmail.com', 'Ethan', 'Johnson', pw, 'Male'),
                     Student('David@gmail.com', 'David', 'Johnson', pw, 'Male'),
                     Student('Michael@gmail.com', 'Michael', 'Brown', pw, 'Male'),
                     Student('Alexander@gmail.com', 'Alexander', 'Brown', pw, 'Male'),
                     Student('Daniel@gmail.com', 'Daniel', 'Brown', pw, 'Male'),
                     Student('Megan@gmail.com', 'Megan', 'Brown', pw, 'Female'),
                     Student('Mia@gmail.com', 'Mia', 'Taylor', pw, 'Female'),
                     Student('Barbara@gmail.com', 'Barbara', 'Taylor', pw, 'Female'),
                     Student('Linda@gmail.com', 'Linda', 'Taylor', pw, 'Female'),
                     Student('Margaret@gmail.com', 'Margaret', 'Taylor', pw, 'Female'),
                     Student('Lily@gmail.com', 'Lily', 'Li', pw, 'Female'),
                     Student('Ava@gmail.com', 'Ava', 'Li', pw, 'Female'),
                     Student('Emily@gmail.com', 'Emily', 'Li', pw, 'Female'),
                     Student('Patricia@gmail.com', 'Patricia', 'Li', pw, 'Female'),
                     Student('Jennifer@gmail.com', 'Jennifer', 'Byrne', pw, 'Female')]
    pw = password()
    student_list2 = [Student('Tamir@outlook.com', 'Tamir', 'Byrne', pw, 'Male'),
                     Student('Hadar@outlook.com', 'Hadar', 'Byrne', pw, 'Female'),
                     Student('Sapir@outlook.com', 'Sapir', 'Roy', pw, 'Female'),
                     Student('Shaked@outlook.com', 'Shaked', 'Roy', pw, 'Female'),
                     Student('Boten@outlook.com', 'Boten', 'Roy', pw, 'Female'),
                     Student('Din@outlook.com', 'Din', 'Roy', pw, 'Male'),
                     Student('Roni@outlook.com', 'Roni', 'Wang', pw, 'Male'),
                     Student('Gal@outlook.com', 'Gal', 'Wang', pw, 'Male'),
                     Student('Oliver@outlook.com', 'Oliver', 'Wang', pw, 'Male'),
                     Student('Jack@outlook.com', 'Jack', 'Wang', pw, 'Male'),
                     Student('Harry@outlook.com', 'Harry', 'Anderson', pw, 'Male'),
                     Student('Thomas@outlook.com', 'Thomas', 'Anderson', pw, 'Male'),
                     Student('George@outlook.com', 'George', 'Anderson', pw, 'Male'),
                     Student('Amelia@outlook.com', 'Amelia', 'Anderson', pw, 'Female'),
                     Student('Isabella@outlook.com', 'Isabella', 'Perets', pw, 'Female'),
                     Student('Mary@outlook.com', 'Mary', 'Perets', pw, 'Female'),
                     Student('Jessica@outlook.com', 'Jessica', 'Perets', pw, 'Female'),
                     Student('Sarah@outlook.com', 'Sarah', 'Cohen', pw, 'Female'),
                     Student('Yael@outlook.com', 'Yael', 'Cohen', pw, 'Female'),
                     Student('Adi@outlook.com', 'Adi', 'Cohen', pw, 'Female'),
                     Student('Matan@outlook.com', 'Matan', 'Cohen', pw, 'Male'),
                     Student('Jake@outlook.com', 'Jake', 'Levi', pw, 'Male'),
                     Student('Jacob@outlook.com', 'Jacob', 'Levi', pw, 'Male'),
                     Student('Ethan@outlook.com', 'Ethan', 'Levi', pw, 'Male'),
                     Student('David@outlook.com', 'David', 'Levi', pw, 'Male'),
                     Student('Michael@outlook.com', 'Michael', 'Green', pw, 'Male'),
                     Student('Alexander@outlook.com', 'Alexander', 'Green', pw, 'Male'),
                     Student('Daniel@outlook.com', 'Daniel', 'Green', pw, 'Male'),
                     Student('Megan@outlook.com', 'Megan', 'Green', pw, 'Female'),
                     Student('Mia@outlook.com', 'Mia', 'Molcho', pw, 'Female'),
                     Student('Barbara@outlook.com', 'Barbara', 'Molcho', pw, 'Female'),
                     Student('Linda@outlook.com', 'Linda', 'Molcho', pw, 'Female'),
                     Student('Margaret@outlook.com', 'Margaret', 'Molcho', pw, 'Female'),
                     Student('Lily@outlook.com', 'Lily', 'Horev', pw, 'Female'),
                     Student('Ava@outlook.com', 'Ava', 'Horev', pw, 'Female'),
                     Student('Emily@outlook.com', 'Emily', 'Horev', pw, 'Female'),
                     Student('Patricia@outlook.com', 'Patricia', 'Horev', pw, 'Female'),
                     Student('Jennifer@outlook.com', 'Jennifer', 'Horev', pw, 'Female')]

    for student in student_list1:
        db.session.add(student)
    db.session.commit()
    for student in student_list2:
        db.session.add(student)
    db.session.commit()
    print(Student.query.all())


def teacher_init():
    pw = password()
    teacher_list = [Teacher('Mali@gmail.com', 'Mali', 'Houri', pw, 'Female'),
                    Teacher('Zohar@gmail.com', 'Zohar', 'Houri', pw, 'Male'),
                    Teacher('Ofir@gmail.com', 'Ofir', 'Bailey', pw, 'Male'),
                    Teacher('Almog@gmail.com', 'Almog', 'Bailey', pw, 'Male'),
                    Teacher('Peleg@gmail.com', 'Peleg', 'Baker', pw, 'Male'),
                    Teacher('Boaz@gmail.com', 'Boaz', 'Carter', pw, 'Male'),
                    Teacher('Iris@gmail.com', 'Iris', 'Carter', pw, 'Female'),
                    Teacher('Shane@gmail.com', 'Shane', 'Cooper', pw, 'Female'),
                    Teacher('Dana@gmail.com', 'Dana', 'Cooper', pw, 'Female'),
                    Teacher('Addison@gmail.com', 'Addison', 'Fisher', pw, 'Female'),
                    Teacher('Abegail@gmail.com', 'Abegail', 'Fisher', pw, 'Female'),
                    Teacher('Lewis@gmail.com', 'Lewis', 'Grant', pw, 'Female'),
                    Teacher('Dan@gmail.com', 'Dan', 'Armstrong', pw, 'Male'),
                    Teacher('Glen@gmail.com', 'Glen', 'Armstrong', pw, 'Male'),
                    Teacher('Antonio@gmail.com', 'Antonio', 'Grant', pw, 'Male')]

    for teacher in teacher_list:
        db.session.add(teacher)
    db.session.commit()
    print(Teacher.query.all())


def course_init():
    course_list = [Course('Algebra 1', 16), Course('English 1', 16), Course('Spanish 1', 2), Course('Calculus 1', 2),
                   Course('Progreming 1', 3), Course('Algebra 2', 3), Course('English 2', 4), Course('Spanish 2', 4),
                   Course('Calculus 2', 5), Course('Progreming 2', 5), Course('Sports 1', 6),
                   Course('Deep Learning 1', 6), Course('C++ 1', 7), Course('Trx 1', 7), Course('Sports 2', 8),
                   Course('Deep Learning 2', 8), Course('C++ 2', 9), Course('Trx 2', 9),
                   Course('Business 1', 10), Course('Management 1', 10), Course('Accounting 1', 11),
                   Course('Marketing 1', 11), Course('Project Management 1', 12), Course('Finance  1', 12),
                   Course('Administration  1', 13), Course('Statistics 1', 13), Course('Engineering 1', 14),
                   Course('Architecture  1', 14), Course('History 1', 15), Course('Literature 1', 15),
                   Course('Maths 1', 16), Course('Psychology 1', 2), Course('Biology 1', 3), Course('Nursing 1', 4),
                   Course('Business 2', 5), Course('Management 2', 6), Course('Accounting 2', 7),
                   Course('Marketing 2', 8), Course('Project Management 2', 9), Course('Literature 2', 10),
                   Course('Finance  2', 11), Course('Administration  2', 12), Course('Statistics 2', 13),
                   Course('Engineering 2', 14), Course('Architecture  2', 15), Course('History 2', 16),
                   Course('Maths 2', 2), Course('Psychology 2', 3), Course('Biology 2', 4), Course('Nursing 2', 5)]

    for course in course_list:
        db.session.add(course)
    db.session.commit()
    print(Course.query.all())


def enrollment_init():
    courses = Course.query.all()
    students = Student.query.all()
    stu_i = first = students[0].id
    last = students[-1].id
    for i in range(0, 15):
        for course in courses:
            enrol1 = Enrollment(course.id, stu_i)
            enrol1.grade = random.randint(45, 100)
            db.session.add(enrol1)
            if stu_i == last:
                stu_i = first
            else:
                stu_i += 1
    db.session.commit()
    print(Enrollment.query.all())


def task_init():
    long_text = """In project management, a task is an activity that needs to be accomplished within 
        a defined period of time or by a deadline to work towards work-related goals. It is a small essential piece of
         a job that serves as a means to differentiate various components of a project. A task can be broken down into 
         assignments which should also have a defined start and end date or a deadline for completion. One or more 
         assignments on a task puts the task under execution. Completion of all assignments on a specific task normally
          renders the task completed. Tasks can be linked together to create dependencies.

        Tasks completion generally requires the coordination of others. Coordinated human interaction takes on the role
        of combining the integration of time, energy, effort, ability, and resources of multiple individuals to meet
         a common goal. Coordination can also be thought of as the critical mechanism that links or ties together the
          efforts on the singular level to that of the larger task being completed by multiple members. Coordination
           allows for the successful completion of the otherwise larger tasks that one might encounter.

            In most projects, tasks may suffer one of two major drawbacks:

            Task dependency: Which is normal as most tasks rely on others to get done. However, this can lead to the 
            stagnation of a project when many tasks cannot get started unless others are finished.
            Unclear understanding of the term complete: For example, if a task is 90% complete, does this mean that 
            it will take only 1/9 of the time already spent on this task to finish it? Although this is mathematically
             sound, it is rarely the case when it comes to practice."""

    courses = Course.query.all()
    for course in courses:
        task = Task('Long Task', long_text, course.id, course.lecturer.id)
        task1 = Task('Task 1', 'hello students this is my first task', course.id, course.lecturer.id)
        task2 = Task('Homework', 'homework task: do questions 1,2,3,4,5,6 from the notebook', course.id, course.lecturer.id)
        task3 = Task('Task 2', 'hello students this is my seconed task', course.id, course.lecturer.id)
        task4 = Task('Homework', 'homework task: do questions 7,8,9 from the notebook', course.id, course.lecturer.id)
        db.session.add(task1)
        db.session.add(task)
        db.session.add(task2)
        db.session.add(task3)
        db.session.add(task4)
        db.session.commit()

    print(Task.query.all())
