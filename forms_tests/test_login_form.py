import unittest
from flask import Flask
from forms.login_form import LoginForm  # Replace `yourapp` with the actual module name

class TestLoginForm(unittest.TestCase):
    def setUp(self):
        """Set up the Flask application for testing."""
        self.app = Flask(__name__)
        self.app.secret_key = "default_key"  # Needed for CSRF protection
        self.client = self.app.test_client()
        self.app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing

    def test_valid_form_submission(self):
        """Test form with valid input data."""
        with self.app.test_request_context():
            form = LoginForm(
                email="test@example.com",
                password="password123"
            )
            self.assertTrue(form.validate())

    def test_missing_email(self):
        """Test form with missing email."""
        with self.app.test_request_context():
            form = LoginForm(
                email="",
                password="password123"
            )
            self.assertFalse(form.validate())
            self.assertIn("This field is required.", form.email.errors)

    def test_invalid_email(self):
        """Test form with invalid email address."""
        with self.app.test_request_context():
            form = LoginForm(
                email="invalid-email",
                password="password123"
            )
            self.assertFalse(form.validate())
            self.assertIn("Invalid email address.", form.email.errors)

    def test_missing_password(self):
        """Test form with missing password."""
        with self.app.test_request_context():
            form = LoginForm(
                email="test@example.com",
                password=""
            )
            self.assertFalse(form.validate())
            self.assertIn("This field is required.", form.password.errors)

if __name__ == "__main__":
    unittest.main()