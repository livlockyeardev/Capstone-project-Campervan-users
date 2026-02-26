from django.urls import path
from .views import (
    CreateBooking,
    CancelBooking,
    BookingConfirmation,
    block_off_availability,
    ManageBookings,
)

urlpatterns = [
    path("book/<slug:slug>/", CreateBooking.as_view(), name="create-booking"),
    path("cancel/<int:pk>/", CancelBooking.as_view(), name="cancel-booking"),
    path("confirmation/<int:pk>/", BookingConfirmation.as_view(), name="booking_confirmation"),
    path("block-off/<slug:slug>/", block_off_availability, name="block-off-availability"),
    path("manage/", ManageBookings.as_view(), name="manage-bookings"),
]