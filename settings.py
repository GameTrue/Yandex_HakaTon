from flask_wtf import FlaskForm
from wtforms import BooleanField, RadioField, SubmitField
from wtforms.validators import DataRequired
 
class SettingsForm(FlaskForm):
    reverse = BooleanField('Сортировать по убыванию')
    sort_type = RadioField(choices=[('date', 'Сортировать по дате добавления'), ('alphabet', 'Сортировать по алфавиту')], default='date')
    submit = SubmitField('Применить изменения')

