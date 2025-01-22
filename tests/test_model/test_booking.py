import pytest
from model import UserModel
from model import SpaceModel
from model import BookingModel
from model import RequestModel
from extension import db
from datetime import date

# Fixture to create a test user
@pytest.fixture
def test_user(app, database):
    with app.app_context():
        user = UserModel(
            username = "Alister",
            password = "password123",
            email = "alister@example.com",
            phone_number = 123456780
        )
    db.session.add(user)
    db.session.commit()
    return user

# Fixture to create a test requester
@pytest.fixture
def test_requester(app, database):
    with app.app_context():
        requester = UserModel(
            username = "Louis",
            password = "password123",
            email = "louis@example.com",
            phone_number = 123456789
        )
    db.session.add(requester)
    db.session.commit()
    return requester

# Fixture to create a test space
@pytest.fixture
def test_space(app, database, test_user):
    with app.app_context():
        space = SpaceModel(
            name = "123 Strand",
            description = "Alister's home",
            location = "Holborn",
            price_per_night = 5000.00,
            owner_id = test_user.id
        )
    db.session.add(space)
    db.session.commit()
    return space

def test_create_booking(app, database, test_user, test_requester, test_space):
    with app.app_context():
        booking = BookingModel(
            space_id = test_space.id,
            requester_id= test_requester.id,
            booking_start_date = date(2025, 1, 25),
            booking_end_date = date(2025, 1, 30)
        )
        db.session.add(booking)
        db.session.commit()
        
        saved_booking = BookingModel.query.filter_by(id = booking.id).first()
        assert saved_booking.id is not None
        assert saved_booking.space_id == test_space.id
        assert saved_booking.requester_id == test_requester.id
        assert saved_booking.booking_start_date == date(2025, 1, 25)
        assert saved_booking.booking_end_date == date(2025, 1, 30)

def test_multiple_bookings(app, database, test_user, test_space):
    with app.app_context():
        booking1 = BookingModel(
            space_id = test_space.id,
            requester_id = test_user.id,
            booking_start_date = date(2025, 1, 25),
            booking_end_date = date(2025, 1, 30)
        )
        db.session.add(booking1)
        db.session.commit()
        
        booking2 = BookingModel(
            space_id = test_space.id,
            requester_id = test_user.id,
            booking_start_date = date(2025, 2, 1),
            booking_end_date = date(2025, 2, 5)
        )
        db.session.add(booking2)
        db.session.commit()
        
        space_bookings = BookingModel.query.filter_by(space_id = test_space.id).all()
        assert len(space_bookings) == 2
        assert booking1 in space_bookings # verify the bookings exist
        assert booking2 in space_bookings