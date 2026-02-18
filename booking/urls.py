from django.urls import path
from . import views

urlpatterns = [
    path("book/<slug:slug>/", views.CreateBooking.as_view(), name="create-booking"),
    path("confirmation/<int:pk>/", views.BookingConfirmation.as_view(), name="booking_confirmation"),
]