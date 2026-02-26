from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.utils.text import slugify
from .utils import geocode_town


NOISE_LEVELS = ((0, "Quiet"), (1, "Moderate"), (2, "Loud"))


class Listing(models.Model):
    """Represents a listing created by a user, containing details about the
    listing such as title, description, location, and pricing.
        Each listing is associated with an author (the user who created it)
        and can have an optional featured image.
        The model also includes fields for geocoding the location to store
        latitude and longitude for map display."""
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )
    featured_image = CloudinaryField('image', default='placeholder')
    description = models.TextField()
    location = models.CharField(max_length=20)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    toilet_available = models.BooleanField(default=False)
    noise_level = models.IntegerField(choices=NOISE_LEVELS, default=0)
    min_nights = models.IntegerField()
    max_nights = models.IntegerField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_on"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.location and (self.latitude is None or self.longitude is None):
            lat, lng = geocode_town(self.location)
            self.latitude = lat
            self.longitude = lng
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}"
