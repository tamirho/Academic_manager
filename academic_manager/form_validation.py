
def sign_up_validation(user_name, user_email, user_password, password_confirmation, user_type):
    if user_password == password_confirmation:
        return True, ""
    else:
        return False, "problem with password"
