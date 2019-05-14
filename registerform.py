from flask_wtf import FlaskForm,  RecaptchaField
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_wtf.file import FileField, FileAllowed, FileRequired


class RegisterForm(FlaskForm):
    username = StringField('*Логин', validators=[DataRequired()])
    password = PasswordField('*Пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегестрироваться')
