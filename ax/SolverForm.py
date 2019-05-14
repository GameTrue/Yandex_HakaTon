from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DateField
from wtforms.widgets import TextArea, TextInput
from wtforms.validators import DataRequired
from wtforms import validators

class SolverForm(FlaskForm):
    task_name = StringField('Название задачи:', validators=[DataRequired()], widget=TextInput())
    code = TextAreaField('Комментарии:', validators=[DataRequired()],widget=TextArea())
    date = StringField('Дата:', validators=[DataRequired()], widget=TextInput())
    aut_name = StringField('Имя автора:', validators=[DataRequired()], widget=TextInput())
    submit = SubmitField('Отправить')