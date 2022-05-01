from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField

from wtforms.validators import DataRequired


class ProfileForm(FlaskForm):
    name = StringField('Имя пользователя', validators=[DataRequired()])
    surname = StringField('Фамилия пользователя', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    submit = SubmitField('Сохранить')
