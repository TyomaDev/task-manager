from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from main.models import User


class TaskForm(FlaskForm):
    title = StringField('Название задачи', validators=[DataRequired(), Length(min=5, max=40)])
    description = TextAreaField('Описание задачи', validators=[DataRequired()])
    submit = SubmitField('Отправить')

class RegistrationForm(FlaskForm):
    username = StringField('ФИО',
                           validators=[DataRequired('Поле обязательно к заполнению'), Length(min=2, max=60)])
    email = StringField('Email',
                        validators=[DataRequired('Поле обязательно к заполнению'),
                                    Email(message='Поле заполнено неверно')])
    password = PasswordField('Пароль', validators=[DataRequired('Поле заполнено неверно')])
    confirm_password = PasswordField('Подтвердите пароль',
                                     validators=[DataRequired('Поле обязательно к заполнению'), EqualTo('password')])
    submit = SubmitField('Создать')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Этот email занят. Пожалуйста, выберите другой.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired('Поле заполнено неверно'), Email(message='Поле заполнено неверно')])
    password = PasswordField('Пароль', validators=[DataRequired('Поле заполнено неверно')])
    remember = BooleanField('Запомнить')
    submit = SubmitField('Войти')
