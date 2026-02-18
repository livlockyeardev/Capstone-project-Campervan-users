from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView
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
        check_in = form.cleaned_data.get("check_in")
        check_out = form.cleaned_data.get("check_out")

        if check_in and check_out:
            nights = (check_out - check_in).days
            min_nights = self.listing.min_nights
            max_nights = self.listing.max_nights

            if min_nights is not None and nights < min_nights:
                form.add_error(
                    "check_out",
                    f"This listing requires a minimum stay of {min_nights} night(s).",
                )

            if max_nights is not None and nights > max_nights:
                form.add_error(
                    "check_out",
                    f"This listing allows a maximum stay of {max_nights} night(s).",
                )

            if form.errors:
                return self.form_invalid(form)

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
    
class ManageBookings(LoginRequiredMixin, ListView):
    model = Booking
    template_name = "booking/manage_bookings.html"
    context_object_name = "bookings"

    def get_queryset(self):
        return (
            Booking.objects
            .select_related("listing")
            .filter(user=self.request.user)
            .order_by("-created_on")
        )