from flask import session
from academic_manager.main.form_validation import *
from academic_manager.models import Student


def clear_user_info_from_session():
    session.pop("user_name", None)
    session.pop("type", None)


def update_user_profile(user_to_update, new_user_name, new_email):
    messages = []
    if user_to_update.user_name != new_user_name:
        if validate_user_name(new_user_name):
            user_to_update.user_name = new_user_name
            db.session.commit()
        else:
            messages.append("User Name already exist")

    if user_to_update.email != new_email:
        if validate_email(new_email):
            user_to_update.email = new_email
            db.session.commit()
        else:
            messages.append("Email already exist")

    return messages


def change_user_password(user_to_update, old_pass, new_pass, pass_confirmation):
    messages = []

    if old_pass != user_to_update.password:
        messages.append("Incorrect old password!")
    elif not validate_password(new_pass, pass_confirmation):
        messages.append("The passwords are not equal!")
    else:
        user_to_update.password = new_pass
        db.session.commit()

    return messages


