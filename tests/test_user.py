import pytest
from model import UserModel
from model import SpaceModel
from model import BookingModel
from model import RequestModel
from extension import db

def test_create_user(app, database):
    with app.app_context():
        user = UserModel(
            username = "Frank",
            password = "password123",
            email = "frank@example.com",
            phone_number = 123456780
        )
    db.session.add(user)
    db.session.commit()
    
    saved_user = UserModel.query.filter_by(username = "Frank").first()
    assert user.id is not None
    assert user.phone_number == 123456780
    assert user.email == "frank@example.com"
    
def test_unique_user_details(app, database):
    with app.app_context():
        # Create the first user
        user = UserModel(
            username = "Frank",
            password = "password123",
            email = "frank@example.com",
            phone_number = 123456780
        )
        db.session.add(user)
        db.session.commit()
    
        # Try creating a user with same email
        with pytest.raises(Exception):
            user2 = UserModel(
                username = "Arthur",
                password = "password123",
                email = "frank@example.com",
                phone_number = 234567890
            )
            db.session.add(user2)
            db.session.commit()

        # Try creating a user with same username
        with pytest.raises(Exception):
            user3 = UserModel(
                username = "Frank",
                password = "password123",
                email = "alister@example.com",
                phone_number = 111111111
            )
            db.session.add(user3)
            db.session.commit()
            
        # Try creating a user with same phone number
        with pytest.raises(Exception):
            user4 = UserModel(
                username = "Alister",
                password = "password123",
                email = "louis@example.com",
                phone_number = 123456780
            )
            db.session.add(user4)
            db.session.commit()