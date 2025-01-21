from sqlalchemy.engine import TupleResult
from sqlalchemy.orm import backref

from extension import db

class BookingModel(db.Model):
    __tablename__ = "bookings"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    space_id = db.Column(db.Integer, db.ForeignKey("space.id"), nullable = False)
    request_id = db.Column(db.Integer, db.ForeignKey("request.id"), nullable = False)
    start_date = db.Column(db.String(200), nullable = False)
    end_date = db.Column(db.String(200), nullable = False)