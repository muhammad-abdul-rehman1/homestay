import os
import django
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from listings.models import User, Listing, Booking

def verify():
    print("Verifying models...")
    
    # Create Host
    host = User.objects.create_user(username='host1', password='password', is_host=True)
    print(f"Created host: {host.username}, is_host={host.is_host}")

    # Create Guest
    guest = User.objects.create_user(username='guest1', password='password')
    print(f"Created guest: {guest.username}, is_host={guest.is_host}")

    # Create Listing
    listing = Listing.objects.create(
        host=host,
        title="Cozy Apartment",
        price_per_night=100.00,
        room_type="entire_place",
        country="USA",
        amenities={"wifi": True, "kitchen": True}
    )
    print(f"Created listing: {listing.title} by {listing.host.username}")

    # Create Booking
    booking = Booking.objects.create(
        listing=listing,
        guest=guest,
        check_in=date(2023, 12, 1),
        check_out=date(2023, 12, 5),
        total_price=400.00
    )
    print(f"Created booking: {booking} for {booking.total_price}")

    print("Verification complete!")

if __name__ == "__main__":
    try:
        verify()
    except Exception as e:
        print(f"Verification failed: {e}")
