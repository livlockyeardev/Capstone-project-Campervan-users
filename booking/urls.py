from django.urls import path
from . import views
from .views import block_off_availability

urlpatterns = [
    path("book/<slug:slug>/", views.CreateBooking.as_view(), name="create-booking"),
    path("cancel/<int:pk>/", views.CancelBooking.as_view(), name="cancel-booking"),
    path("confirmation/<int:pk>/", views.BookingConfirmation.as_view(), name="booking_confirmation"),
    path("block-off/<slug:slug>/", block_off_availability, name="block-off-availability"),
    path("manage/", views.ManageBookings.as_view(), name="manage-bookings"),
]