from geopy.geocoders import Nominatim


def geocode_town(town_name: str):
    geolocator = Nominatim(user_agent="capstone-listings-map")
    loc = geolocator.geocode(f"{town_name}, UK", timeout=10)
    if not loc:
        return None, None
    return loc.latitude, loc.longitude