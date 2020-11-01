from flask import Flask
from academic_manager.extensions import db, bcrypt, login_manager, mail
from academic_manager.config import Config


login_manager.login_view = 'main.login'
login_manager.login_message_category = 'danger'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    app.jinja_env.add_extension('jinja2.ext.loopcontrols')

    from academic_manager.main.routes import main
    from academic_manager.admin.routes import admin
    from academic_manager.students.routes import students
    from academic_manager.teachers.routes import teachers
    from academic_manager.courses.routes import courses
    from academic_manager.errors.handlers import errors

    app.register_blueprint(main)
    app.register_blueprint(admin)
    app.register_blueprint(students)
    app.register_blueprint(teachers)
    app.register_blueprint(courses)
    app.register_blueprint(errors)

    return app
