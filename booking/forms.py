from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Booking


class BookingForm(forms.ModelForm):
    """Form for creating an instance of the Booking model."""
    class Meta:
        model = Booking
        fields = ("check_in", "check_out", "registration_plate")
        widgets = {
            "check_in": forms.DateInput(attrs={"type": "date"}),
            "check_out": forms.DateInput(attrs={"type": "date"}),
        }
     
    # form constructor calls parent class constructor, controls form layout
    # and adds submit button
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit("submit", "Book"))

        # The clean method validates the check-in and check-out dates:
        # - Check-in and check-out cannot be in the past
        # - Check-out must be after check-in
    def clean(self):
        from datetime import date
        cleaned_data = super().clean()
        check_in = cleaned_data.get("check_in")
        check_out = cleaned_data.get("check_out")
        today = date.today()
        if check_in:
            if check_in < today:
                self.add_error("check_in", "Check-in date cannot be in the past.")
        if check_out:
            if check_out < today:
                self.add_error("check_out", "Check-out date cannot be in the past.")
        if check_in and check_out and check_out <= check_in:
            self.add_error("check_out", "Check-out must be after check-in.")
        return cleaned_data
