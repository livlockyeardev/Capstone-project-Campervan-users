from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "listing", "user", "check_in", "check_out", "total_price", "status", "created_on")
    list_filter = ("status", "created_on")
    search_fields = ("user__username", "listing__title", "registration_plate")