from flask import redirect, url_for, render_template, request, session, flash, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from academic_manager.extensions import db, bcrypt, restricted
from academic_manager.models import User
from academic_manager.forms import RegistrationForm, LoginForm, UpdateUserForm
from academic_manager.main.utilities import *
from academic_manager.students.utilities import *
from datetime import datetime
from academic_manager.main.db_init import init_db

main = Blueprint('main', __name__, template_folder="templates")


@main.route("/")
@main.route("/home/")
def home():
    # init_db()
    best_student = get_best_student()
    current_date = datetime.now()
    return render_template("home.html", best_student=best_student, current_date=current_date)


@main.route("/login/", methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        flash("Already logged in!", "warning")
        return redirect(url_for("main.home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            session.permanent = True  # todo delete if not need session
            flash("Logged in successfully!", "success")
            return redirect(next_page) if next_page else redirect(url_for("main.home"))
        else:
            flash("The Email or Password is invalid", "danger")
            return redirect(url_for("main.login", form=form))

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


@main.route("/profile/")
@login_required
def profile():
    image_file = url_for('static', filename='profile_pics/' + current_user.profile_img)
    return render_template('profile.html', image_file=image_file)


@main.route("/update/<int:user_id>/", methods=['POST', 'GET'])
@restricted(role=["admin", "current_user"])
def update_user_profile(user_id):
    form = UpdateUserForm()
    user = User.query.get_or_404(user_id)
    if form.validate_on_submit():

        if form.picture.data:

            # Resize and save picture in users folder
            pic_file = save_picture(form.picture.data)

            # Removes the previous image from the repository
            remove_profile_picture(user.profile_img)
            user.profile_img = pic_file

        name = user.first_name
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.email = form.email.data
        user.gender = form.gender.data
        db.session.commit()

        flash(f"{name}'s profile has been updated!", 'success')
        return redirect(url_for('main.profile'))

    elif request.method == 'GET':
        form.first_name.data = user.first_name
        form.last_name.data = user.last_name
        form.email.data = user.email
        form.gender.data = user.gender

    return render_template('update_user_profile.html', user=user, form=form)


# todo create an option to choose one of the pictures from the default folder
@main.route("/profile_pic_gallery/")
@login_required
def get_profile_picture_gallery():
    item_lst = os.listdir(os.path.join(app.root_path, 'static/profile_pics/default'))
    gallery_lst = [url_for('static', filename='profile_pics/default/' + item) for item in item_lst]
    print(gallery_lst)
    return render_template('profile_pic_gallery.html', gallery_lst=gallery_lst)
