from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .models import Booking
from .forms import BookingForm
from listing.models import Listing


class CreateBooking(LoginRequiredMixin, CreateView):
    model = Booking
    form_class = BookingForm
    template_name = "booking/create_booking.html"
    success_url = reverse_lazy("home")

    def dispatch(self, request, *args, **kwargs):
        self.listing = get_object_or_404(Listing, slug=kwargs["slug"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.listing = self.listing
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["listing"] = self.listing
        return context