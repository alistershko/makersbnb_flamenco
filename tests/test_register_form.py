import unittest
from flask import Flask, render_template_string
from forms.register_form import RegisterForm  # Replace `yourapp` with the actual app module

class TestRegisterForm(unittest.TestCase):
    def setUp(self):
        """Set up the Flask application for testing."""
        self.app = Flask(__name__)
        self.app.secret_key = "default_key"  # Needed for CSRF protection
        self.client = self.app.test_client()
        self.app.config['WTF_CSRF_ENABLED'] = False

    def test_valid_form_submission(self):
        """Test form with valid input data."""
        with self.app.test_request_context():
            form = RegisterForm(
                username="testuser",
                email="test@example.com",
                password="password123",
                confirm_password="password123",
                phone_number=1234567890
            )
            if not form.validate():
              print(form.errors)  # Print validation errors for debugging
            self.assertTrue(form.validate())

    def test_invalid_email(self):
        """Test form with an invalid email address."""
        with self.app.test_request_context():
            form = RegisterForm(
                username="testuser",
                email="invalid-email",
                password="password123",
                confirm_password="password123",
                phone_number=1234567890
            )
            self.assertFalse(form.validate())
            self.assertIn("Invalid email address.", form.email.errors)

    def test_password_mismatch(self):
        """Test form with mismatched passwords."""
        with self.app.test_request_context():
            form = RegisterForm(
                username="testuser",
                email="test@example.com",
                password="password123",
                confirm_password="wrongpassword",
                phone_number=1234567890
            )
            self.assertFalse(form.validate())
            self.assertIn("Field must be equal to password.", form.confirm_password.errors)

    def test_missing_username(self):
        """Test form with missing username."""
        with self.app.test_request_context():
            form = RegisterForm(
                username="",
                email="test@example.com",
                password="password123",
                confirm_password="password123",
                phone_number=1234567890
            )
            self.assertFalse(form.validate())
            self.assertIn("This field is required.", form.username.errors)

    def test_missing_email(self):
        """Test form with missing email."""
        with self.app.test_request_context():
            form = RegisterForm(
                username="testuser",
                email="",
                password="password123",
                confirm_password="password123",
                phone_number=1234567890
            )
            self.assertFalse(form.validate())
            self.assertIn("This field is required.", form.email.errors)

    def test_missing_phone_number(self):
        """Test form with missing phone number."""
        with self.app.test_request_context():
            form = RegisterForm(
                username="testuser",
                email="test@example.com",
                password="password123",
                confirm_password="password123",
                # No phone_number provided
            )
            self.assertFalse(form.validate())
            self.assertIn("This field is required.", form.phone_number.errors)


    def test_password_too_short(self):
        """Test form with a password that is too short."""
        with self.app.test_request_context():
            form = RegisterForm(
                username="testuser",
                email="test@example.com",
                password="123",
                confirm_password="123",
                phone_number=1234567890
            )
            self.assertFalse(form.validate())
            self.assertIn("Field must be at least 6 characters long.", form.password.errors)


if __name__ == "__main__":
    unittest.main()