from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from .models import Booking
from .forms import BookingForm
from listing.models import Listing


class CreateBooking(LoginRequiredMixin, CreateView):
    model = Booking
    form_class = BookingForm
    template_name = "booking/create_booking.html"

    def dispatch(self, request, *args, **kwargs):
        self.listing = get_object_or_404(Listing, slug=kwargs["slug"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.listing = self.listing
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("booking_confirmation", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["listing"] = self.listing
        return context


class BookingConfirmation(LoginRequiredMixin, DetailView):
    model = Booking
    template_name = "booking/booking_confirmation.html"
    context_object_name = "booking"

    def get_queryset(self):
        return Booking.objects.select_related("listing").filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["listing"] = self.object.listing
        return context