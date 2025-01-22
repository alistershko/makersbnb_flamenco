from model import UserModel, SpaceModel, BookingModel, RequestModel
from extension import db
from datetime import date

def create_user(username, email, phone_number):
    user = UserModel(
        username=username,
        password="password123",
        email=email,
        phone_number=phone_number
    )
    db.session.add(user)
    db.session.commit()
    return user

def create_space(name, description, location, price_per_night, owner_id):
    space = SpaceModel(
        name=name,
        description=description,
        location=location,
        price_per_night=price_per_night,
        owner_id=owner_id
    )
    db.session.add(space)
    db.session.commit()
    return space

def create_request(space_id, requester_id, message, start_date, end_date):
    request = RequestModel(
        space_id=space_id,
        requester_id=requester_id,
        message=message,
        booking_start_date=start_date,
        booking_end_date=end_date
    )
    db.session.add(request)
    db.session.commit()
    return request

def create_booking(space_id, requester_id, start_date, end_date):
    booking = BookingModel(
        space_id=space_id,
        requester_id=requester_id,
        booking_start_date=start_date,
        booking_end_date=end_date
    )
    db.session.add(booking)
    db.session.commit()
    return booking