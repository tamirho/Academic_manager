import os
import secrets
from PIL import Image
from flask import current_app, url_for
from academic_manager.extensions import db, mail
from academic_manager.models import Student, Teacher, Admin
from flask_mail import Message


def make_new_user(email, first_name, last_name, hashed_password, gender, role):
    if role == "admin":
        new_user = Admin(email, first_name, last_name, hashed_password, gender)
    elif role == "teacher":
        new_user = Teacher(email, first_name, last_name, hashed_password, gender)
    else:
        new_user = Student(email, first_name, last_name, hashed_password, gender)

    db.session.add(new_user)
    db.session.commit()


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    pic_name = random_hex + f_ext
    pic_path = os.path.join(current_app.root_path, 'static/profile_pics/users', pic_name)

    output_size = (200, 200)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(pic_path)

    return 'users/' + pic_name


def remove_profile_picture(pic_name):
    if pic_name.startswith("users/"):
        pic_path = os.path.join(current_app.root_path, 'static/profile_pics', pic_name)
        if os.path.isfile(pic_path):
            os.remove(pic_path)


def send_reset_password_email(user):
    token = user.get_reset_password_token()
    msg = Message('Password Reset Request',
                  sender=os.environ.get('EMAIL_USERNAME'),
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('main.reset_password_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)
    return