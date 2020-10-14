from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from wtforms.validators import DataRequired


class NewEnrollmentForm(FlaskForm):
    enrollment = SelectField('Courses', validators=[DataRequired()], coerce=int, validate_choice=False)
    submit = SubmitField('Enroll Now')
