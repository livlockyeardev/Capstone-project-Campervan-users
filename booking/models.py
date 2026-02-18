from django.db import models
from django.contrib.auth.models import User
from listing.models import Listing


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

    def __str__(self):
        return f"{self.user.username} - {self.listing.title} ({self.check_in} to {self.check_out})"
    
    @property
    def owner(self):
        """Returns the owner of the listing"""
        return self.listing.author
