from sqlalchemy.engine import TupleResult
from sqlalchemy.orm import backref

from extension import db

class SpaceModel(db.Model):
    __tablename__ = "spaces"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(200), nullable = False)
    description = db.Column(db.Text, nullable = False)
    location = db.Column(db.String(200), nullable = False, unique = True)
    price_per_night = db.Column(db.Float, nullable = False)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete = "CASCADE"), nullable = False)

    
   
    bookings = db.relationship("BookingModel", backref = "space", lazy = True, cascade="all, delete")

    requests = db.relationship("RequestModel", backref = "space", lazy = True, cascade="all, delete")



