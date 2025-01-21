from sqlalchemy.engine import TupleResult
from sqlalchemy.orm import backref

from extension import db

class UserModel(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String(200), nullable = False, unique = True)
    password = db.Column(db.String(200), nullable = False)
    email = db.Column(db.String(200), nullable = False, unique = True)

    # owner = UserModel()
    # owner.spaces(location = "kingscross")
    # space = SpaceModel()
    # space.owner().email()
    #

    spaces = db.relationship("SpaceModel", backref = "owner", lazy = True, cascade="all, delete")
#   as user you want to check your spaces listed
    bookings = db.relationship("BookingModel", backref = "user", lazy = True, cascade="all, delete")
#    as a user you want to check your bookings
    requests = db.relationship("RequestModel", backref = "user", lazy = True, cascade="all, delete")
#    as tenant you want to check your requests






