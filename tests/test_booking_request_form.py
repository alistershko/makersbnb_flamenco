import unittest
from flask import Flask
from forms.booking_request_form import BookingRequestForm  # Replace `yourapp` with the actual module name
from datetime import date

class TestBookingRequestForm(unittest.TestCase):
    def setUp(self):
        """Set up the Flask application for testing."""
        self.app = Flask(__name__)
        self.app.secret_key = "default_key"  # Needed for CSRF protection
        self.client = self.app.test_client()
        self.app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing

    def test_valid_form_submission(self):
        """Test form with valid input data."""
        with self.app.test_request_context():
            form = BookingRequestForm(
                booking_start_date=date.today(),
                booking_end_date=date.today(),
                message="Looking forward to booking this space!"
            )
            self.assertTrue(form.validate())

    def test_missing_booking_start_date(self):
        """Test form with missing booking start date."""
        with self.app.test_request_context():
            form = BookingRequestForm(
                booking_start_date=None,
                booking_end_date=date.today(),
                message="Looking forward to booking this space!"
            )
            self.assertFalse(form.validate())
            self.assertIn("This field is required.", form.booking_start_date.errors)

    def test_missing_booking_end_date(self):
        """Test form with missing booking end date."""
        with self.app.test_request_context():
            form = BookingRequestForm(
                booking_start_date=date.today(),
                booking_end_date=None,
                message="Looking forward to booking this space!"
            )
            self.assertFalse(form.validate())
            self.assertIn("This field is required.", form.booking_end_date.errors)

    def test_message_too_long(self):
        """Test form with a message exceeding the maximum length."""
        long_message = "a" * 301  # 301 characters, exceeds max length
        with self.app.test_request_context():
            form = BookingRequestForm(
                booking_start_date=date.today(),
                booking_end_date=date.today(),
                message=long_message
            )
            self.assertFalse(form.validate())
            self.assertIn("Field cannot be longer than 300 characters.", form.message.errors)

    def test_empty_message(self):
        """Test form with an empty optional message."""
        with self.app.test_request_context():
            form = BookingRequestForm(
                booking_start_date=date.today(),
                booking_end_date=date.today(),
                message=""
            )
            self.assertTrue(form.validate())

if __name__ == "__main__":
    unittest.main()

