from . import views
from django.urls import path

urlpatterns = [
    path('', views.ListingList.as_view(), name='home'),
    path('create/', views.ListingCreate.as_view(), name='create-listing'),
    path('managelisting/', views.ManageListings.as_view(), name='manage-listings'),
    path('edit/<slug:slug>/', views.ListingUpdate.as_view(), name='edit-listing'),
    path('delete/<slug:slug>/', views.ListingDelete.as_view(), name='delete-listing'),
    path('<slug:slug>/', views.ListingDetail.as_view(), name='listing-detail'),
]