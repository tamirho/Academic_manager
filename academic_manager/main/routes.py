from flask import redirect, render_template, request, flash, Blueprint, url_for, current_app
from flask_login import login_user, current_user, logout_user, login_required
from academic_manager.extensions import bcrypt, restricted
from academic_manager.main.forms import (RegistrationForm, LoginForm, UpdateUserForm, ProfilePictureForm,
                                         ResetPasswordForm, ResetPasswordRequestForm)
from academic_manager.main.utilities import *
from academic_manager.students.utilities import *
from datetime import datetime
from academic_manager.models import User
from academic_manager.main.db_init import init_db

main = Blueprint('main', __name__, template_folder="templates")


@main.route("/init_db")
def main_db_init():
    init_db()
    return redirect(url_for("main.home"))


@main.route("/")
@main.route("/home/")
def home():
    if current_user.is_authenticated:
        best_student = get_best_student()
        current_date = datetime.now()
        return render_template("home.html", best_student=best_student, current_date=current_date)
    else:
        return render_template("index.html")


@main.route("/login/", methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        flash("Already logged in!", "warning")
        return redirect(url_for("main.home"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()

        # Validate the password if the user exist
        if user and bcrypt.check_password_hash(user.password, form.password.data):

            # Check if teacher ia approved by the admin
            if user.is_teacher and not user.approved:
                flash(f"{user.email} is not approved yet by the admin", "danger")
                return redirect(url_for("main.home"))

            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash("Logged in successfully!", "success")
            return redirect(next_page) if next_page else redirect(url_for("main.home"))

        else:
            flash("The Email or Password is invalid", "danger")
            return redirect(url_for("main.login"))

    return render_template("login.html", form=form)


@main.route("/register/", methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        flash("Already logged in!", "warning")
        return redirect(url_for("main.home"))
    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        make_new_user(form.email.data, form.first_name.data, form.last_name.data,
                      hashed_password, form.gender.data, form.role.data)
        flash(f'Account created for {form.first_name.data}! You can login now', 'success')
        return redirect(url_for('main.login'))

    return render_template('register.html', form=form)


@main.route("/logout/")
@login_required
def logout():
    current_user.update_last_seen()
    logout_user()
    return redirect(url_for("main.home"))


@main.route("/profile/<int:user_id>")
@login_required
def profile(user_id):
    user = User.query.get_or_404(user_id)
    image_file = url_for('static', filename='profile_pics/' + user.profile_img)
    return render_template('profile.html', user=user, image_file=image_file)


# todo fix the problem when admin update other users
@main.route("/update/<int:user_id>/", methods=['POST', 'GET'])
@restricted(role=["admin", "current_user"])
def update_user_profile(user_id):
    form = UpdateUserForm(user_id=user_id)
    user = User.query.get_or_404(user_id)

    if form.validate_on_submit():

        # Profile picture handling
        if form.picture.data:

            # Resize and save picture in users folder
            pic_file = save_picture(form.picture.data)

            # Removes the previous image from the repository
            remove_profile_picture(user.profile_img)
            user.profile_img = pic_file

        name = user.first_name
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.email = form.email.data.lower()
        user.gender = form.gender.data
        db.session.commit()

        flash(f"{name}'s profile has been updated!", 'success')
        return redirect(url_for('main.profile', user_id=user_id))

    elif request.method == 'GET':
        form.first_name.data = user.first_name
        form.last_name.data = user.last_name
        form.email.data = user.email
        form.gender.data = user.gender

    return render_template('update_user_profile.html', user=user, form=form)


@main.route("/profile-pic-gallery/", methods=['POST', 'GET'])
@login_required
def profile_picture_gallery():
    item_lst = os.listdir(os.path.join(current_app.root_path, 'static/profile_pics/default'))
    form = ProfilePictureForm()

    if form.validate_on_submit():
        remove_profile_picture(current_user.profile_img)
        current_user.profile_img = "default/" + form.images.data
        db.session.commit()

        flash('Your profile image has been updated!', 'success')
        return redirect(url_for('main.profile', user_id=current_user.id))

    elif request.method == "GET":
        form.images.choices = item_lst

    return render_template('profile_pic_gallery.html', form=form)


@main.route("/delete_user/<int:user_id>")
@restricted(role=["admin", "current_user"])
def delete_user(user_id):
    user_to_del = User.query.get_or_404(user_id)

    # User deleting his profile
    if current_user.id == user_id:
        logout_user()
        user_to_del.delete_from_db()
        flash("Your account has been deleted", "success")
        return redirect(url_for("main.home"))

    # Admin deleting other user profile
    if current_user.is_admin:
        flash(f"{user_to_del.email} has been deleted", "success")
        is_teacher = user_to_del.is_teacher
        user_to_del.delete_from_db()
        return redirect(url_for("admin.admin_teachers")) if is_teacher \
            else redirect(url_for("admin.admin_students"))


@main.route("/reset-password/", methods=['POST', 'GET'])
def reset_password_request():
    if current_user.is_authenticated:
        flash("Already logged in!", "warning")
        return redirect(url_for("main.home"))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_password_email(user)
        flash("An email has been sent to your account with password reset instructions.", "info")
        return redirect(url_for("main.login"))

    return render_template('reset_password_request.html', form=form)


@main.route("/reset-password/<token>/", methods=['POST', 'GET'])
def reset_password_token(token):
    if current_user.is_authenticated:
        flash("Already logged in!", "warning")
        return redirect(url_for("main.home"))

    user = User.verify_reset_password_token(token)
    if not user:
        flash("Your token is invalid or has expired", "warning")
        return redirect(url_for("main.reset_password_request"))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has been updated! You can login now', 'success')
        return redirect(url_for('main.login'))
    return render_template('reset_password_token.html', form=form)
