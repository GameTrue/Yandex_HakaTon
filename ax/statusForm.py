from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField


class StatusForm(FlaskForm):
    select = SelectField('Выберите статус', choices=[('Выполняется', 'Выполняется'), ('Отложено', 'Отложено'), ('Выполнено', 'Выполнено')])
    people = SelectField('Выберите статус', choices=[('user2', 'user2')])
    submit = SubmitField('Сохранить')