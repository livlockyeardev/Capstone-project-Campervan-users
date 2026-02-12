from . import views
from django.urls import path

urlpatterns = [
    path('listings/', views.listings, name='listings'),]