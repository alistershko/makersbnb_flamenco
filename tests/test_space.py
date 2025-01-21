import pytest
from model import UserModel
from model import SpaceModel
from model import BookingModel
from model import RequestModel
from extension import db
from datetime import datetime

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

# The actual test
def test_create_space(app, database, test_user):
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
        
        saved_space = SpaceModel.query.filter_by(name = "123 Strand").first()
        assert saved_space.id is not None
        assert saved_space.description == "Alister's home"
        assert saved_space.location == "Holborn"
        assert saved_space.price_per_night == 5000.00