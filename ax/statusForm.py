from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, TextAreaField
from wtforms.widgets import TextArea, TextInput
from wtforms.validators import DataRequired
from flask import Flask, render_template, request, redirect, session
import json
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SECRET_KEY'] = 'e70lIUUoXRKlXc5VUBmiJ9Hdi'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

ADMINS = json.loads(open('static/admins.txt', 'r', encoding='utf-8').read())

class YandexLyceumStudent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(80), unique=False, nullable=False)
    surname = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    passwordtwo = db.Column(db.String(120), unique=False, nullable=False)

    def __repr__(self):
        return '<YandexLyceumStudent {} {} {} {}>'.format(
            self.id, self.username, self.name, self.surname)

    def __repr__(self):
        return '<SolutionAttempt {} {} {}>'.format(
            self.id, self.task, self.status)


dat = [('None', 'None')]
all = YandexLyceumStudent.query.all()
for i in all:
    sender = i.username
    dat.append((sender, sender))


class StatusForm(FlaskForm):
    str = TextAreaField('Название задачи:', widget=TextArea())
    select = SelectField('Выберите статус', choices=[('Выполняется', 'Выполняется'), ('Отложено', 'Отложено'), ('Выполнено', 'Выполнено')])
    people = SelectField('Выберите статус', choices=dat)
    submit = SubmitField('Сохранить')