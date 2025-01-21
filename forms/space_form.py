from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FloatField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class SpaceForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()])
    location = StringField("Location", validators=[DataRequired()])
    price_per_night = FloatField("Price per night", validators=[DataRequired()])
    submit = SubmitField("Submit")