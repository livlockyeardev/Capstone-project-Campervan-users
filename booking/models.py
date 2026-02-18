from django.db import models
from django.contrib.auth.models import User
from listing.models import Listing
from django.core.exceptions import ValidationError
from decimal import Decimal


class Booking(models.Model):
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

    class Meta:
        ordering = ['-created_on']

    def _recalculate_total_price(self):
        """Compute total_price when listing and dates are available."""
        if self.listing_id and self.check_in and self.check_out and self.check_out > self.check_in:
            nights = (self.check_out - self.check_in).days
            nightly_rate = self.listing.price_per_night or Decimal("0.00")
            self.total_price = nightly_rate * Decimal(nights)

    def clean(self):
        if self.check_in and self.check_out and self.check_out <= self.check_in:
            raise ValidationError("Check-out must be after check-in.")

    def save(self, *args, **kwargs):
        # Ensure total_price is populated before full_clean() runs field validation
        self._recalculate_total_price()

        # Prevent "cannot be null" from masking other validation errors
        if self.total_price is None:
            self.total_price = Decimal("0.00")

        if self.listing_id:
            self.full_clean()
        super().save(*args, **kwargs)


