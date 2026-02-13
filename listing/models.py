from django.db import models
from django.contrib.auth.models import User


NOISE_LEVELS = ((0, "Quiet"), (1, "Moderate"), (2, "Loud"))
# Create your models here.


class Listing(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )
    description = models.TextField()
    location = models.CharField(max_length=20)
    toilet_available = models.BooleanField(default=False)
    noise_level = models.IntegerField(choices=NOISE_LEVELS, default=0)
    min_nights = models.IntegerField()
    max_nights = models.IntegerField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"{self.title}"