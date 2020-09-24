from flask import redirect, url_for, render_template, request, session, flash
from academic_manager import app, db
from academic_manager.form_validation import *
from academic_manager.admin_funcs import *

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/admin/", methods=['POST', 'GET'])
def admin():
    student_list = Student.query.all()
    teacher_list = Teacher.query.all()
    courses_list = Course.query.all()
    return render_template("admin.html", student_list=student_list, teacher_list=teacher_list,
                           courses_list=courses_list)


@app.route("/admin/add_course/", methods=['POST', 'GET'])
def add_course():
    if request.method == "POST":
        course_name = request.form["course_name"]
        teacher_name = request.form["teacher_name"]
        if validate_course_name(course_name):
            make_new_course_by_names(course_name, teacher_name)
            flash("The course is added to the list", "success")
            return redirect(url_for("admin"))
        else:
            flash("That Course name is invalid", "warning")
            return redirect(url_for("add_course"))
    else:
        teacher_list = Teacher.query.all()
        return render_template("add_course.html", teacher_list=teacher_list)


@app.route("/teacher/")
def teacher():
    teacher_profile = Teacher.query.filter_by(user_name=session["user_name"]).first()
    return render_template("teacher.html", teacher=teacher_profile)


@app.route("/student/")
def student():
    student_profile = Student.query.filter_by(user_name=session["user_name"]).first()
    return render_template("student.html", student=student_profile)


@app.route("/login/", methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        session.permanent = True
        user_name = request.form["user_name"]
        user_password = request.form["user_password"]
        user_type = user_authentication(user_name, user_password)
        if not user_type == "none":
            session["user_name"] = user_name
            session["type"] = user_type
            flash("Logged in successfully!", "success")
            return redirect(url_for("user"))
        else:
            flash("The username or password is invalid", "danger")
            return redirect(url_for("login"))
    else:
        if "user_name" in session:
            flash("Already logged in!", "warning")
            return redirect(url_for("user"))
        return render_template("login.html")


@app.route("/sign-up/", methods=['POST', 'GET'])
def sign_up():
    if request.method == "POST":
        user_name = request.form["user_name"]
        user_email = request.form["user_email"]
        user_password = request.form["user_password"]
        password_confirmation = request.form["password_confirmation"]
        user_type = request.form["user_type"]
        check_flag, messages = sign_up_validation(user_name, user_email, user_password, password_confirmation)
        if check_flag:
            make_new_user(user_name, user_email, user_password, user_type)
            flash("Sign up successfully! you can login now", "info")
            return redirect(url_for("login"))
        else:
            for message in messages:
                flash(message, "danger")
            return redirect(url_for("sign_up"))
    else:
        if "user_name" in session:
            flash("Already logged in!", "warning")
            return redirect(url_for("user"))
        return render_template("sign_up.html")


@app.route("/user/")
def user():

    if "type" in session:
        user_name = session["user_name"]
        if session["type"] == "admin":
            return redirect(url_for("admin"))
        elif session["type"] == "teacher":
            return redirect(url_for("teacher", user_name=user_name))
        else:
            return redirect(url_for("student", user_name=user_name))
    else:
        flash("You need to login first", "danger")
        return redirect(url_for("home"))


@app.route("/logout/")
def logout():
    if "user_name" in session:
        user_name = session["user_name"]
        flash(f"{user_name}, you logged out successfully!", "success")
        session.pop("user_name", None)
        session.pop("type", None)
    return redirect(url_for("home"))
