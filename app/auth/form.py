from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import ValidationError,DataRequired,Length


class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired(),Length(min=4)])
    password = StringField("password", validators=[DataRequired(),Length(min=4)])

    