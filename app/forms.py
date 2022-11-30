from app import app
from flask_wtf import FlaskForm
import wtforms as ws
from .models import Transactions, User

class TransactionsForm(FlaskForm):
    period = ws.StringField('Период', validators=[ws.validators.DataRequired(), ])
    value = ws.IntegerField('Сумма')
    status = ws.StringField('Статус')
    unit = ws.StringField('Валюта')
    subject = ws.StringField('Комментарии проводки')

class UserForm(FlaskForm):
    username = ws.StringField('Имя пользователя', validators=[
        ws.validators.DataRequired(),
        ws.validators.Length(min=4, max=20)
    ])
    password = ws.PasswordField('Пароль', validators=[
        ws.validators.DataRequired(),
        ws.validators.Length(min=8, max=24)
    ])