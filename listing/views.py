from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Listing
from .forms import ListingForm


# Create your views here.
class ListingList(generic.ListView):
    queryset = Listing.objects.all().order_by("-created_on")
    template_name = "listing/index.html"


class ListingDetail(generic.DetailView):
    model = Listing
    template_name = "listing/listing_detail.html"
    context_object_name = "listing"


class ListingCreate(LoginRequiredMixin, generic.CreateView):
    model = Listing
    form_class = ListingForm
    template_name = "listing/create_listing.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
   

class ManageListings(LoginRequiredMixin, generic.ListView):
    model = Listing
    template_name = "listing/manage_listings.html"
    context_object_name = "listings"

    def get_queryset(self):
        return Listing.objects.filter(author=self.request.user).order_by("-created_on")


class ListingUpdate(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Listing
    form_class = ListingForm
    template_name = "listing/edit_listing.html"
    success_url = reverse_lazy("manage-listings")

    def test_func(self):
        listing = self.get_object()
        return self.request.user == listing.author


class ListingDelete(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Listing
    template_name = "listing/delete_listing.html"
    success_url = reverse_lazy("manage-listings")

    def test_func(self):
        listing = self.get_object()
        return self.request.user == listing.author