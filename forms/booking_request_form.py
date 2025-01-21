from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, DateField, TextAreaField
from wtforms.validators import DataRequired, Length

class BookingRequestForm(FlaskForm):
    # space_id = IntegerField("Space ID", validators=[DataRequired()])
    # register_id = IntegerField("Register ID", validators=[DataRequired()])
    message = TextAreaField(
        "Message (Optional)",
        validators=[Length(max=300)],
        description="Provide any additional comments or reasons for booking.",
    )
    booking_start_date = DateField("Booking Start Date", validators=[DataRequired()])
    booking_end_date = DateField("Booking End Date", validators=[DataRequired()])
    submit = SubmitField("Submit Request")