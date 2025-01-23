from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, EmailField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp
from email_validator import *

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=20)])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    phone_number = StringField("Phone Number", validators=[
        DataRequired(),
        Regexp(r'^\+?[1-9]\d{1,14}$', message="Invalid phone number format")
    ])
    submit = SubmitField("Sign Up")

