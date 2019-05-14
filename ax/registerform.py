from flask_wtf import FlaskForm,  RecaptchaField
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_wtf.file import FileField, FileAllowed, FileRequired


class RegisterForm(FlaskForm):
    user_name = StringField('Username:', validators=[DataRequired()])
    password = StringField('Password:', validators=[DataRequired()])
    email = StringField('Email:', validators=[Email()])
    name = StringField('Name:', validators=[DataRequired()])
    surname = StringField('Surname:', validators=[DataRequired()])
    submit = SubmitField('Отправить')
