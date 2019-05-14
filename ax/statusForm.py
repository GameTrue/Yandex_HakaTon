from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField


class StatusForm(FlaskForm):
    select = SelectField('Выберите статус',choices=[('Выполняется', 'Выполняется'), ('Отложено', 'Отложено'), ('Выполнено', 'Выполнено')])
    submit = SubmitField('Сохранить')