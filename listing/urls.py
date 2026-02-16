from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.ListingList.as_view(), name='home'),
    path('create/', views.ListingCreate.as_view(), name='create-listing'),
    path('managelisting/', views.ManageListings.as_view(), name='manage-listings'),
]