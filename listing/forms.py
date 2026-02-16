from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Listing


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = (
            "title",
            "featured_image",
            "description",
            "location",
            "toilet_available",
            "noise_level",
            "min_nights",
            "max_nights",
            "price_per_night",
        )

        labels = {
            "title": "Title (Maximum Five Words)",
            "featured_image": "Display Image",
            "description": "Description (Maximum 200 Words)",
            "location": "Location (Maximum 20 Characters)",
            "toilet_available": "Facilities Available?",
            "noise_level": "Noise Level",
            "min_nights": "Minimum Nights",
            "max_nights": "Maximum Nights",
            "price_per_night": "Price Per Night (We suggest keeping a price under £5 if no facilities are available and under £10 if there are.)",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Create Listing"))