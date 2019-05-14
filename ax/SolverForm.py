from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.widgets import TextArea, TextInput
from wtforms.validators import DataRequired

class SolverForm(FlaskForm):
    task_name = StringField('Название задачи:', validators=[DataRequired()], widget=TextInput())
    code = TextAreaField('Код:', validators=[DataRequired()],widget=TextArea())
    submit = SubmitField('Отправить')