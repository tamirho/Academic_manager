from flask import session


def clear_user_info_from_session():
    session.pop("user_name", None)
    session.pop("type", None)
    return
