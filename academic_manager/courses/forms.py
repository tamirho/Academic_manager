from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (StringField, SubmitField, SelectField, TextAreaField)
from wtforms.validators import DataRequired, Length, ValidationError, Optional
from academic_manager.models import Course


class CourseForm(FlaskForm):
    teacher = SelectField('Teacher', validators=[DataRequired()], coerce=int, validate_choice=False)
    course = StringField('Course Name', validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Add Course')

    def validate_course(self, course):
        course_exist = Course.query.filter_by(course_name=course.data).first()
        if course_exist:
            raise ValidationError('That Course name is taken, Please use another one.')


class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=20)])
    content = TextAreaField('Content', validators=[Optional()])
    file = FileField('Add File',
                     validators=[Optional(),
                                 FileAllowed(['pdf', 'doc', 'docx', 'xls', 'xlsx'], 'Document only!')
                                 ])
    file_name = StringField('File Name', validators=[Optional(), Length(min=1, max=20)])
    submit = SubmitField('Submit')




