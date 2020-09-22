from flask import redirect, url_for, render_template, request, session, flash
from academic_manager import app, db
from academic_manager.models import Student
from academic_manager.form_validation import *


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/admin/")
def admin():
    return render_template("admin.html")


@app.route("/teacher/")
def teacher():
    return render_template("teacher.html")


@app.route("/student/")
def student():
    return render_template("student.html")


@app.route("/login/", methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        session.permanent = True
        user_name = request.form["user_name"]
        user_password = request.form["user_password"]
        session["user_name"] = user_name
        session["type"] = "student"
        flash("Logged in successfully!", "success")
        return redirect(url_for("user"))
    else:
        if "user_name" in session:
            flash("Already logged in!", "warning")
            return redirect(url_for("user"))
        return render_template("login.html")


@app.route("/sign-up/", methods=['POST', 'GET'])
def sign_up():
    if request.method == "POST":
        user_name = request.form["user_name"]
        user_email = request.form["user_email"]  # todo use regex to check the email
        user_password = request.form["user_password"]  # todo create check pass function
        password_confirmation = request.form["password_confirmation"]
        user_type = request.form["user_type"]
        check_flag, problem = sign_up_validation(user_name, user_email, user_password,
                                                 password_confirmation, user_type)
        if check_flag:
            session["user_name"] = user_name  # todo crate a function to activate and deactivate session
            session["type"] = user_type

            new_user = Student(user_name, user_email, user_password)
            db.session.add(new_user)
            db.session.commit()
            flash("Sign up successfully!", "success")
            return redirect(url_for("user"))
        else:
            flash(problem, "danger")
            return redirect(url_for("sign_up"))
    else:
        return render_template("sign_up.html")


@app.route("/user/")
def user():
    if "type" in session:
        if session["type"] == "admin":
            return redirect(url_for("admin"))
        elif session["type"] == "teacher":
            return redirect(url_for("teacher"))
        else:
            return redirect(url_for("student"))
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
