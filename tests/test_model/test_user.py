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
        
        #verify Frank has been created
        assert UserModel.query.filter_by(username = "Frank").first() is not None
    
        # Try creating a user with same email
        with pytest.raises(Exception, match="duplicate key value violates unique constraint"):
            user2 = UserModel(
                username = "Arthur",
                password = "password123",
                email = "frank@example.com",
                phone_number = 234567890
            )
            db.session.add(user2)
            db.session.commit()
        db.session.rollback()

        # Try creating a user with same username
        with pytest.raises(Exception, match="duplicate key value violates unique constraint"):
            user3 = UserModel(
                username = "Frank",
                password = "password123",
                email = "alister@example.com",
                phone_number = 111111111
            )
            db.session.add(user3)
            db.session.commit()
        db.session.rollback()
            
        # Try creating a user with same phone number
        with pytest.raises(Exception, match="duplicate key value violates unique constraint"):
            user4 = UserModel(
                username = "Alister",
                password = "password123",
                email = "louis@example.com",
                phone_number = 123456780
            )
            db.session.add(user4)
            db.session.commit()
        db.session.rollback()
            
        assert UserModel.query.count() == 1, f"Expected 1 user, found {UserModel.query.count()}"

