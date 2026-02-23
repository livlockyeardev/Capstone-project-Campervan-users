from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView
from .models import Booking
from .forms import BookingForm
from listing.models import Listing
from django.contrib.auth.decorators import login_required
from datetime import datetime


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

            # Overlapping booking check
            overlapping = Booking.objects.filter(
                listing=self.listing,
                status__in=["confirmed"],
                check_in__lt=check_out,
                check_out__gt=check_in,
            )
            if overlapping.exists():
                form.add_error(
                    "check_in",
                    "These dates overlap with an existing booking. Please choose different dates.",
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
    

@login_required
def block_off_availability(request, slug):
    listing = get_object_or_404(Listing, slug=slug, author=request.user)
    if request.method == "POST":
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        if start_date and end_date:
            try:
                check_in = datetime.strptime(start_date, "%Y-%m-%d").date()
                check_out = datetime.strptime(end_date, "%Y-%m-%d").date()
                Booking.objects.create(
                    listing=listing,
                    user=request.user,
                    check_in=check_in,
                    check_out=check_out,
                    status="confirmed",  # or "blocked" if you want a custom status
                    registration_plate="",
                )
            except Exception:
                pass  # Optionally add error handling/messages
    return redirect(reverse("listing-availability", kwargs={"slug": listing.slug}))


class CancelBooking(LoginRequiredMixin, DetailView):
    model = Booking

    def post(self, request, *args, **kwargs):
        booking = self.get_object()
        booking.status = "cancelled"
        booking.save()
        return redirect("manage-bookings")