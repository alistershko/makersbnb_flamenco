from sqlalchemy.engine import TupleResult
from sqlalchemy.orm import backref
from datetime import *

from extension import db

class BookingModel(db.Model):
    __tablename__ = "bookings"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    space_id = db.Column(db.Integer, db.ForeignKey("spaces.id"), nullable = False)
    requester_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    booking_start_date = db.Column(db.Date, nullable = False)
    booking_end_date = db.Column(db.Date, nullable = False)