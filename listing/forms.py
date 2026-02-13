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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Create Listing"))