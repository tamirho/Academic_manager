from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
from flask_mail import Mail
from flask import abort
from functools import wraps


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
mail = Mail()


def restricted(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                return login_manager.unauthorized()
            if current_user.role in role:
                return func(*args, **kwargs)
            if "current_user" in role and 'user_id' in kwargs:
                if kwargs['user_id'] == current_user.id:
                    return func(*args, **kwargs)
            abort(403)
        return wrapper
    return decorator
