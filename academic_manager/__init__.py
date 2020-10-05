from flask import Flask
from datetime import timedelta
from academic_manager.extensions import db

app = Flask(__name__)
app.secret_key = "my secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['EXPLAIN_TEMPLATE_LOADING'] = True
app.permanent_session_lifetime = timedelta(minutes=10)

db.init_app(app)

from academic_manager.main.routes import main
from academic_manager.admin.routes import admin
from academic_manager.students.routes import students
from academic_manager.teachers.routes import teachers
from academic_manager.courses.routes import courses

app.register_blueprint(main)
app.register_blueprint(admin)
app.register_blueprint(students)
app.register_blueprint(teachers)
app.register_blueprint(courses)

