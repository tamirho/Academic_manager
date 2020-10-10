from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (StringField, PasswordField, SubmitField, BooleanField,
                     RadioField, SelectField, TextAreaField)
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from flask_login import current_user
from academic_manager.models import User, Course


class RegistrationForm(FlaskForm):
    first_name = StringField('First Name',
                             validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name',
                            validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    gender = RadioField('Gender', validators=[DataRequired()], choices=['Male', 'Female'], default='Male')
    role = RadioField('Role', validators=[DataRequired()], choices=[('student', 'Student'), ('teacher', 'Teacher')],
                      default='Student')

    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That Email is taken, Please use another one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateUserForm(FlaskForm):
    first_name = StringField('First Name',
                             validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name',
                            validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    gender = RadioField('Gender', validators=[DataRequired()], choices=['Male', 'Female'])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_email(self, email):
        if current_user.email != email.data:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That Email is taken, Please use another one.')


class NewEnrollmentForm(FlaskForm):
    enrollment = SelectField('Courses', validators=[DataRequired()], coerce=int, validate_choice=False)
    submit = SubmitField('Enroll Now')


class AddCourseForm(FlaskForm):
    teacher = SelectField('Teacher', validators=[DataRequired()], coerce=int, validate_choice=False)
    course = StringField('Course Name', validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Add Course')

    def validate_course(self, course):
        course = Course.query.filter_by(course_name=course.data).first()
        if course:
            raise ValidationError('That Course name is taken, Please use another one.')


class AddTaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=20)])
    content = TextAreaField('Task Content', validators=[Optional(), Length(max=200)])
    file = FileField('Add File', validators=[Optional(), FileAllowed(['pdf', 'doc', 'docx'])])
    submit = SubmitField('Add Course')
