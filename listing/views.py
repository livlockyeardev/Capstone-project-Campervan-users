from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Listing
from .forms import ListingForm
from django.db.models import Count, Q
from django.views.generic import ListView
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from booking.models import Booking
from django.contrib import messages


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
   

class ManageListings(LoginRequiredMixin, ListView):
    model = Listing
    template_name = "listing/manage_listings.html"
    context_object_name = "listings"

    def get_queryset(self):
        return (
            Listing.objects
            .filter(author=self.request.user)
            .annotate(
                pending_bookings_count=Count(
                    "bookings",
                    filter=Q(bookings__status="pending")
                )
            )
            .order_by("-created_on")
        )


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


@login_required
def listing_availability(request, slug):
    listing = get_object_or_404(Listing, slug=slug, author=request.user)

    if request.method == "POST":
        booking_id = request.POST.get("booking_id")
        new_status = request.POST.get("status")
        owner_message = (request.POST.get("owner_message") or "").strip()

        booking = get_object_or_404(
            Booking,
            id=booking_id,
            listing=listing,
            status="pending",
        )

        if new_status not in {"confirmed", "cancelled"}:
            messages.error(request, "Invalid status selected.")
            return redirect(reverse("listing-availability", kwargs={"slug": listing.slug}))

        booking.status = new_status
        booking.owner_message = owner_message
        booking.save(update_fields=["status", "owner_message"])

        messages.success(request, "Booking updated and message saved.")
        return redirect(reverse("listing-availability", kwargs={"slug": listing.slug}))

    confirmed_qs = Booking.objects.filter(listing=listing, status="confirmed").order_by("check_in")
    pending_bookings = Booking.objects.filter(listing=listing, status="pending").order_by("check_in")

    confirmed_events = [
        {
            "title": "Booked",
            "start": b.check_in.isoformat(),
            "end": (b.check_out + timedelta(days=1)).isoformat(),  # FullCalendar end is exclusive
            "allDay": True,
        }
        for b in confirmed_qs
    ]

    return render(
        request,
        "listing/listing_availability.html",
        {
            "listing": listing,
            "confirmed_events": confirmed_events,
            "pending_bookings": pending_bookings,
        },
    )

class ListingMapView(generic.TemplateView):
    template_name = "listing/map_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["map_listings"] = list(
            Listing.objects
            .exclude(latitude__isnull=True)
            .exclude(longitude__isnull=True)
            .values("title", "slug", "latitude", "longitude", "location")
        )
        return context