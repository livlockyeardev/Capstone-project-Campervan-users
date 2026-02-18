from django.db.models import Count
from .models import Booking


def pending_listing_bookings_count(request):
    if not request.user.is_authenticated:
        return {
            "pending_listing_bookings_count": 0,
            "pending_bookings_by_listing": {},
        }

    pending_qs = Booking.objects.filter(
        listing__author=request.user,
        status="pending",
    )

    total_count = pending_qs.count()

    by_listing = {
        row["listing_id"]: row["count"]
        for row in pending_qs.values("listing_id").annotate(count=Count("id"))
    }

    return {
        "pending_listing_bookings_count": total_count,  
        "pending_bookings_by_listing": by_listing,       
    }