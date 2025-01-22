import unittest
from flask import Flask
from forms.space_form import SpaceForm

class TestSpaceForm(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.secret_key = "default_key"
        self.client = self.app.test_client()
        self.app.config['WTF_CSRF_ENABLED'] = False

    def test_valid_form_submission(self):
        with self.app.test_request_context():
            form = SpaceForm(
                name = "A nice house",
                description = "Little house on the priarie",
                location = "Mountain, UK",
                price_per_night = 45.33
            )
        self.assertTrue(form.validate())

    def test_invalid_name(self):
        with self.app.test_request_context():
            form = SpaceForm(
                name = "",
                description = "Little house on the priarie",
                location = "Mountain, UK",
                price_per_night = 45.33
            )
        self.assertFalse(form.validate())

    def test_invalid_description(self):
        with self.app.test_request_context():
            form = SpaceForm(
                name = "A nice house",
                description = "",
                location = "Mountain, UK",
                price_per_night = 45.33
            )
        self.assertFalse(form.validate())

    def test_invalid_location(self):
        with self.app.test_request_context():
            form = SpaceForm(
                name = "A nice house",
                description = "Little house on the priarie",
                location = "",
                price_per_night = 45.33
            )
        self.assertFalse(form.validate())

    def test_invalid_price_datatype(self):
        with self.app.test_request_context():
            form = SpaceForm(
                name = "A nice house",
                description = "Little house on the priarie",
                location = "Mountain, UK",
                price_per_night = None
            )
        if not form.validate():
            print(form.errors)
        self.assertFalse(form.validate())