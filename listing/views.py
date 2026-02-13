from django.shortcuts import render
from django.views import generic
from .models import Listing


# Create your views here.
class ListingList(generic.ListView):
    queryset = Listing.objects.all().order_by("-created_on")
    template_name = "listing/index.html"