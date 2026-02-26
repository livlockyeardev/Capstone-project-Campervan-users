from django.db import models
from django.contrib.auth.models import User
from listing.models import Listing
from django.core.exceptions import ValidationError
from decimal import Decimal


class Booking(models.Model):
    """Represents a booking made by a user for a specific listing.
       Each booking is linked to a Listing (the place being booked)
       and a User (the person making the booking).
       Stores the check-in and check-out dates for the reservation.
       Optionally records a vehicle registration plate for the booking.
       Calculates and stores the total price for the stay.
       Automatically records the date and time when the booking was created.
       Tracks the status of the booking, which can be 'pending', 'confirmed', or 'cancelled'.
       Allows the listing owner to add an optional message to the booking (owner_message).
    """
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    check_in = models.DateField()
    check_out = models.DateField()
    registration_plate = models.CharField(max_length=20, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('confirmed', 'Confirmed'),
            ('cancelled', 'Cancelled'),
        ],
        default='pending'
    )
    owner_message = models.TextField(blank=True, default="")

    # Meta class to specify default ordering of bookings by creation date (newest first).
    class Meta:
        ordering = ['-created_on']

    def _recalculate_total_price(self):
        """This function calculates the total price for the booking
        based on the listing's price per night and the number of nights booked.
        - It checks if the booking has an associated listing and valid check-in and check-out dates"""
        if self.listing_id and self.check_in and self.check_out and self.check_out > self.check_in:
            nights = (self.check_out - self.check_in).days
            nightly_rate = self.listing.price_per_night or Decimal("0.00")
            self.total_price = nightly_rate * Decimal(nights)

    def clean(self):
        if self.check_in and self.check_out and self.check_out <= self.check_in:
            raise ValidationError("Check-out must be after check-in.")

    def save(self, *args, **kwargs):
        # Ensures total_price is populated before saving.
        self._recalculate_total_price()

        # Set total_price to 0.00 if it is None to avoid validation errors when the field is required
        if self.total_price is None:
            self.total_price = Decimal("0.00")

        if self.listing_id:
            self.full_clean()
        super().save(*args, **kwargs)
