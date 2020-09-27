from flask import redirect, url_for, render_template, request, session, flash, Blueprint
from academic_manager import db
from academic_manager.main.form_validation import *
from academic_manager.main.utilities import *

main = Blueprint('main', __name__, template_folder="templates")


@main.route("/")
def home():
    return render_template("home.html")


@main.route("/login/", methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        session.permanent = True
        user_name = request.form["user_name"]
        user_password = request.form["user_password"]
        user_type = user_authentication(user_name, user_password)
        if user_type == "disapproved":
            flash("You have not received approval from the admin", "warning")
            return redirect(url_for("main.login"))
        elif not user_type == "none":
            session["user_name"] = user_name
            session["type"] = user_type
            flash("Logged in successfully!", "success")
            return redirect(url_for("main.home"))
        else:
            flash("The username or password is invalid", "danger")
            return redirect(url_for("main.login"))
    else:
        if "user_name" in session:
            flash("Already logged in!", "warning")
            return redirect(url_for("main.user"))
        return render_template("login.html")


@main.route("/sign-up/", methods=['POST', 'GET'])
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
            return redirect(url_for("main.login"))
        else:
            for message in messages:
                flash(message, "danger")
            return redirect(url_for("main.sign_up"))
    else:
        if "user_name" in session:
            flash("Already logged in!", "warning")
            return redirect(url_for("main.user"))
        return render_template("sign_up.html")


@main.route("/user/")
def user():

    if "type" in session:
        user_name = session["user_name"]
        if session["type"] == "admin":
            return redirect(url_for("admin.admin_panel"))
        elif session["type"] == "teacher":
            return redirect(url_for("teachers.teacher", user_name=user_name))
        else:
            return redirect(url_for("students.student", user_name=user_name))
    else:
        flash("You need to login first", "danger")
        return redirect(url_for("main.home"))


@main.route("/logout/")
def logout():
    if "user_name" in session:
        user_name = session["user_name"]
        flash(f"{user_name}, you logged out successfully!", "success")
        clear_user_info_from_session()  # todo check if session.clear() is better for me?
    return redirect(url_for("main.home"))
