from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Listing
from .forms import ListingForm


# Create your views here.
class ListingList(generic.ListView):
    queryset = Listing.objects.all().order_by("-created_on")
    template_name = "listing/index.html"


class ListingCreate(LoginRequiredMixin, generic.CreateView):
    model = Listing
    form_class = ListingForm
    template_name = "listing/create_listing.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)