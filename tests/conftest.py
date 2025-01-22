import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from extension import db
from model.user import UserModel
from model.space import SpaceModel
from model.booking import BookingModel
from model.request import RequestModel

@pytest.fixture(scope="function")
def app(): # Create a Flask test application
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/makersbnb_db_test'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TESTING'] = True
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope="function")
def database(app):
    return db