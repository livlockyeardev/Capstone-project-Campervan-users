from django.test import TestCase
from django.utils import timezone
from booking.forms import BookingForm
from datetime import timedelta


class BookingFormTest(TestCase):
    def setUp(self):
        self.today = timezone.now().date()
        self.tomorrow = self.today + timedelta(days=1)
        self.day_after = self.today + timedelta(days=2)

    def test_valid_data(self):
        form = BookingForm(data={
            'check_in': self.tomorrow,
            'check_out': self.day_after,
            'registration_plate': 'ABC1234',
        })
        self.assertTrue(form.is_valid())

    def test_check_in_in_past(self):
        form = BookingForm(data={
            'check_in': self.today - timedelta(days=1),
            'check_out': self.day_after,
            'registration_plate': 'ABC1234',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('check_in', form.errors)
        self.assertIn('in the past', form.errors['check_in'][0])

    def test_check_out_in_past(self):
        form = BookingForm(data={
            'check_in': self.tomorrow,
            'check_out': self.today - timedelta(days=1),
            'registration_plate': 'ABC1234',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('check_out', form.errors)
        self.assertIn('in the past', form.errors['check_out'][0])

    def test_check_out_before_check_in(self):
        form = BookingForm(data={
            'check_in': self.day_after,
            'check_out': self.tomorrow,
            'registration_plate': 'ABC1234',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('check_out', form.errors)
        self.assertIn('after check-in', form.errors['check_out'][0])