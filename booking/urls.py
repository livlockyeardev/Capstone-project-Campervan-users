from django.urls import path
from . import views

urlpatterns = [
    path("book/<slug:slug>/", views.CreateBooking.as_view(), name="create-booking"),
]