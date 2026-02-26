from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView
from .models import Booking
from .forms import BookingForm
from listing.models import Listing
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib import messages


class CreateBooking(LoginRequiredMixin, CreateView):
    """
    Handles the creation of a new booking for a listing.
    - Ensures the user is logged in.
    - Loads the relevant listing based on the slug in the URL.
    - Validates that the booking dates meet the listing's minimum and maximum night requirements.
    - Checks for overlapping confirmed bookings and prevents double-booking.
    - Adds appropriate error messages for invalid input or booking conflicts.
    - On success, associates the booking with the current user and listing, and displays a success message.
    """
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
                messages.error(self.request, "Booking could not be created. Please fix the errors and try again.")
                return self.form_invalid(form)

        form.instance.user = self.request.user
        form.instance.listing = self.listing
        messages.success(self.request, "Booking created successfully.")
        return super().form_valid(form)

    # Returns the URL to redirect to after a successful booking.
    # Redirects the user to the booking confirmation page for the newly created booking.
    def get_success_url(self):
        return reverse_lazy("booking_confirmation", kwargs={"pk": self.object.pk})

    # Takes the current listing and its confirmed
    # booking events to display in a calendar.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["listing"] = self.listing
        # Build confirmed_events for calendar
        from datetime import timedelta
        confirmed_qs = Booking.objects.filter(listing=self.listing, status="confirmed").order_by("check_in")
        confirmed_events = []
        for booking in confirmed_qs:
            confirmed_events.append({
                "title": "Booked",
                "start": booking.check_in.isoformat(),
                "end": (booking.check_out + timedelta(days=1)).isoformat(),
                "allDay": True,
                "color": "#d4edda",
                "textColor": "#155724",
            })
        context["confirmed_events"] = confirmed_events
        return context


class BookingConfirmation(LoginRequiredMixin, DetailView):
    """
    Displays the booking confirmation page for a user's booking.
    - Ensures only the user who made the booking can view the confirmation.
    - Loads the booking and its associated listing for display in the template.
    - Adds the listing to the context for use in the confirmation template.
    """
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
    """Displays a list of the user's bookings for management.
    - Ensures the user is logged in.
    - Bookings ordered by creation date."""
    model = Booking
    template_name = "booking/manage_bookings.html"
    context_object_name = "bookings"

    def get_queryset(self):
        # Only show bookings made by the user where they are NOT the owner of the listing
        return (
            Booking.objects
            .select_related("listing")
            .filter(user=self.request.user)
            .exclude(listing__author=self.request.user)
            .order_by("-created_on")
        )


@login_required
# Allows a listing owner to block off availability by creating a new Booking instance for specific dates.
# The booking is created with status set to 'confirmed' and an empty registration plate.
# Validates date input and prevents invalid or reversed date ranges.
# Login decorator ensures only authenticated users can access this view.
def block_off_availability(request, slug):
    listing = get_object_or_404(Listing, slug=slug, author=request.user)
    if request.method == "POST":
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        if start_date and end_date:
            try:
                check_in = datetime.strptime(start_date, "%Y-%m-%d").date()
                check_out = datetime.strptime(end_date, "%Y-%m-%d").date()
                if check_in >= check_out:
                    messages.error(request, "Start date must be before end date.")
                    return redirect(reverse("listing-availability", kwargs={"slug": listing.slug}))
                Booking.objects.create(
                    listing=listing,
                    user=request.user,
                    check_in=check_in,
                    check_out=check_out,
                    status="confirmed", 
                    registration_plate="",
                )
            except Exception:
                messages.error(request, "Invalid date format.")
                return redirect(reverse("listing-availability", kwargs={"slug": listing.slug}))
    return redirect(reverse("listing-availability", kwargs={"slug": listing.slug}))


class CancelBooking(LoginRequiredMixin, DetailView):
    """Allows a user to cancel their booking by changing its status to 'cancelled'.
    - Ensures the user is logged in and returns a message confirming the cancellation."""
    model = Booking

    def post(self, request, *args, **kwargs):
        booking = self.get_object()
        booking.status = "cancelled"
        booking.save()
        messages.success(request, "Booking cancelled successfully.")
        return redirect("manage-bookings")