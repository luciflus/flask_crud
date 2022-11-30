from app import app
from flask_wtf import FlaskForm
import wtforms as ws
from .models import Course, Student
from datetime import date, time, datetime
import datetime


class StudentForm(FlaskForm):
    name = ws.StringField('ФИО студента', validators=[ws.validators.DataRequired(), ])
    birth_date = ws.DateField('Дата рождения', validators=[ws.validators.DataRequired(), ])
    phone_number = ws.TelField('Номер телефона', validators=[
        ws.validators.DataRequired(),
        ws.validators.Length(min=10, max=13)
    ])
    course_id = ws.SelectField('Курс', choices=[])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.course_choices = []
        with app.app_context():
            for course in Course.query.all():
                self.course_choices.append((course.id, course.course_name))
        self._fields['course_id'].choices = self.course_choices

    def validate_name(self, field):
        list_1 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u',
                  'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
                  'R', 'S', 'T', 'X', 'Y', 'Z', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '{', '}',
                  '[', ']', '1', '2', '3', '4', '5', '6', '7', '8', '9'
                  ]
        for check in field.data:
            if check in list_1:
                raise ws.ValidationError(
                    'ФИО студента не должно содержать спецсимволов, цифр и должно быть только на русском')

    def validate_phone_number(self, field):
        if field.data[0] != "+":
            raise ws.ValidationError('Номер телефона должен начинаться с +')
        for phone in field.data[1:]:
            if not phone.isdigit():
                raise ws.ValidationError('После знака + должны идти только цифры')

    def validate_birth_date(self, field):
        if datetime.datetime.today().year - field.data.year < 18:
            raise ws.ValidationError('Студенты младше 18 лет не зачисляются на курсы')

class CourseForm(FlaskForm):
    course_name = ws.StringField('Название курса', validators=[ws.validators.DataRequired(), ])
    course_duration = ws.IntegerField('Продолжительность курса', validators=[ws.validators.DataRequired(), ])

class UserForm(FlaskForm):
    username = ws.StringField('Имя пользователя', validators=[
        ws.validators.DataRequired(),
        ws.validators.Length(min=4, max=20)
    ])
    password = ws.PasswordField('Пароль', validators=[
        ws.validators.DataRequired(),
        ws.validators.Length(min=8, max=24)
    ])