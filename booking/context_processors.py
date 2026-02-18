from .models import Booking


def pending_listing_bookings_count(request):
    if not request.user.is_authenticated:
        return {"pending_listing_bookings_count": 0}

    count = Booking.objects.filter(
        listing__author=request.user,
        status="pending",
    ).count()

    return {"pending_listing_bookings_count": count}