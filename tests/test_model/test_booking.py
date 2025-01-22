import pytest
from model import UserModel
from model import SpaceModel
from model import BookingModel
from model import RequestModel
from extension import db
from datetime import date
from tests.test_model.factories import create_user, create_space, create_request, create_booking

# Fixture to create a test user
@pytest.fixture(autouse=True)
def app_context(app):
    with app.app_context():
        yield

@pytest.fixture
def setup_test_data(app):
    with app.app_context():
        owner = create_user("Alister", "alister@example.com", 123456789)
        requester = create_user("Frank", "frank@example.com", 987654321)
        space = create_space("Space1", "A space", "Location1", 100, owner.id)

        yield {
            "owner": owner,
            "requester": requester,
            "space": space
        }

        db.session.query(BookingModel).delete()
        db.session.query(RequestModel).delete()
        db.session.commit()
    
    
def test_create_booking(app, setup_test_data):
    with app.app_context():
        start_date = date(2025, 1, 25)
    end_date = date(2025, 1, 30)
    
    test_booking = create_booking(
        setup_test_data["space"].id,
        setup_test_data["requester"].id,
        start_date,
        end_date
    )
    
    assert test_booking.id is not None
    assert test_booking.space_id == setup_test_data["space"].id
    assert test_booking.requester_id == setup_test_data["requester"].id
    assert test_booking.booking_start_date == start_date
    assert test_booking.booking_end_date == end_date

def test_multiple_bookings(app, setup_test_data):
    with app.app_context():
        booking1 = create_booking(
            setup_test_data["space"].id,
            setup_test_data["requester"].id,
            date(2025, 1, 25),
            date(2025, 1, 30)
        )

        booking2 = create_booking(
            setup_test_data["space"].id,
            setup_test_data["requester"].id,
            date(2025, 2, 1),
            date(2025, 2, 5)
        )
    
        assert booking1.id is not None
        assert booking2.id is not None
        assert booking1.requester_id == booking2.requester_id
        assert BookingModel.query.count() == 2, f"Expected 2 bookings, got {BookingModel.query.count()}"