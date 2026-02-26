
from django.urls import path
from .views import (
    ListingList,
    ListingCreate,
    ListingMapView,
    ManageListings,
    listing_availability,
    ListingUpdate,
    ListingDelete,
    ListingDetail,
)

urlpatterns = [
    path('', ListingList.as_view(), name='home'),
    path('create/', ListingCreate.as_view(), name='create-listing'),
    path('map/', ListingMapView.as_view(), name='listing-map'),
    path('managelisting/', ManageListings.as_view(), name='manage-listings'),
    path("availability/<slug:slug>/", listing_availability, name="listing-availability"),
    path('edit/<slug:slug>/', ListingUpdate.as_view(), name='edit-listing'),
    path('delete/<slug:slug>/', ListingDelete.as_view(), name='delete-listing'),
    path('<slug:slug>/', ListingDetail.as_view(), name='listing-detail'),
]