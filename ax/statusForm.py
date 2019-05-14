from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField


class StatusForm(FlaskForm):
    select = SelectField('Выберите статус',choices=[('На проверке', 'На проверке'), ('Отклонено', 'Отклонено'), ('Зачтено', 'Зачтено')])
    submit = SubmitField('Сохранить')