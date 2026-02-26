from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Listing


class ListingForm(forms.ModelForm):
    """Form for creating an instance of the Listing model.
    - Validates that minimum nights is less than maximum nights and both are greater than 0.
    - Validates that price per night is not negative."""
    def clean(self):
        cleaned_data = super().clean()
        min_nights = cleaned_data.get('min_nights')
        max_nights = cleaned_data.get('max_nights')
        price = cleaned_data.get('price_per_night')
        if min_nights is not None and max_nights is not None:
            if min_nights <= 0 or max_nights <= 0:
                raise forms.ValidationError('Minimum and maximum nights must both be greater than 0.')
            if min_nights >= max_nights:
                raise forms.ValidationError('Minimum nights must be less than maximum nights.')
        if price is not None and price < 0:
            raise forms.ValidationError('Price cannot be negative.')
        return cleaned_data

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
# Labels for form fields and a widget for the description field to use a textarea with 5 rows.
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
        widgets = {
            "description": forms.Textarea(attrs={"rows": 5}),
        }

  # form constructor calls parent class constructor, controls form layout and adds submit button
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Create Listing"))