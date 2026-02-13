from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.ListingList.as_view(), name='home'),
    path("accounts/", include("allauth.urls")),
]