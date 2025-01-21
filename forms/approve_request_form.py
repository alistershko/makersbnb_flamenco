from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length

class ApproveRequestForm(FlaskForm):
    # requester_id = IntegerField("Requester ID", validators=[DataRequired()])
    approval_status = SelectField(
        "Approval Status",
        choices=[("approved", "Approved"), ("rejected", "Rejected")],
        validators=[DataRequired()],
    )
    notes = TextAreaField(
        "Notes (Optional)",
        validators=[Length(max=300)],
        description="Provide any additional comments or reasons for approval/rejection.",
    )
    submit = SubmitField("Submit Approval")
