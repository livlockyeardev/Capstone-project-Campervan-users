
from django.test import TestCase
from listing.forms import ListingForm


class ListingFormTest(TestCase):
    def setUp(self):
        self.valid_data = {
            "title": "Test Listing",
            "featured_image": None,  # Assume optional or handled by model default
            "description": "A nice place to stay.",
            "location": "London",
            "toilet_available": True,
            "noise_level": 1,
            "min_nights": 2,
            "max_nights": 5,
            "price_per_night": 10,
        }

    def test_valid_form(self):
        form = ListingForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_min_nights_greater_than_max_nights(self):
        data = self.valid_data.copy()
        data["min_nights"] = 6
        data["max_nights"] = 5
        form = ListingForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("Minimum nights must be less than maximum nights.", form.errors["__all__"])

    def test_negative_min_nights(self):
        data = self.valid_data.copy()
        data["min_nights"] = -1
        form = ListingForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("Minimum and maximum nights must both be greater than 0.", form.errors["__all__"])

    def test_negative_max_nights(self):
        data = self.valid_data.copy()
        data["max_nights"] = -2
        form = ListingForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("Minimum and maximum nights must both be greater than 0.", form.errors["__all__"])

    def test_negative_price(self):
        data = self.valid_data.copy()
        data["price_per_night"] = -5
        form = ListingForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("Price cannot be negative.", form.errors["__all__"])
