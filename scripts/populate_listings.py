import os
import django
import shutil
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from listings.models import Listing, User, Review

def create_listings():
    # Create a host user if not exists
    host, created = User.objects.get_or_create(username='host', email='host@example.com')
    if created:
        host.set_password('password')
        host.save()

    # Create a guest user for reviews
    guest, created = User.objects.get_or_create(username='guest', email='guest@example.com')
    if created:
        guest.set_password('password')
        guest.save()

    listings_data = [
        {
            'title': 'Malibu, California',
            'price_per_night': 435,
            'room_type': 'entire_place',
            'country': 'USA',
            'category': 'beach',
            'image_url': 'https://images.unsplash.com/photo-1499793983690-e29da59ef1c2?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'latitude': 34.0259,
            'longitude': -118.7798
        },
        {
            'title': 'Whitefish, Montana',
            'price_per_night': 210,
            'room_type': 'entire_place',
            'country': 'USA',
            'category': 'cabins',
            'image_url': 'https://images.unsplash.com/photo-1518780664697-55e3ad937233?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'latitude': 48.4111,
            'longitude': -114.3376
        },
        {
            'title': 'Milan, Italy',
            'price_per_night': 130,
            'room_type': 'entire_place',
            'country': 'Italy',
            'category': 'views',
            'image_url': 'https://images.unsplash.com/photo-1502005229766-52830154f318?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'latitude': 45.4642,
            'longitude': 9.1900
        },
        {
            'title': 'Bali, Indonesia',
            'price_per_night': 180,
            'room_type': 'entire_place',
            'country': 'Indonesia',
            'category': 'castles', # Using castles for variety as per user request
            'image_url': 'https://images.unsplash.com/photo-1525113990976-399835c43838?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            'latitude': -8.4095,
            'longitude': 115.1889
        }
    ]

    for data in listings_data:
        listing, created = Listing.objects.get_or_create(
            title=data['title'],
            defaults={
                'host': host,
                'price_per_night': data['price_per_night'],
                'room_type': data['room_type'],
                'country': data['country'],
                'category': data['category'],
                'latitude': data.get('latitude'),
                'longitude': data.get('longitude')
            }
        )
        
        if created:
            print(f"Created listing: {listing.title}")
            # Create a sample review
            Review.objects.create(
                listing=listing,
                user=guest,
                rating=5,
                comment=f"Amazing stay at {listing.title}! Highly recommended."
            )
            
            # Download and save image
            try:
                response = requests.get(data['image_url'])
                if response.status_code == 200:
                    img_temp = NamedTemporaryFile(delete=True)
                    img_temp.write(response.content)
                    img_temp.flush()
                    listing.image.save(f"{listing.title.replace(' ', '_')}.jpg", File(img_temp))
                    print(f"Saved image for {listing.title}")
            except Exception as e:
                print(f"Error saving image for {listing.title}: {e}")
        else:
            print(f"Listing already exists: {listing.title}")
            # Update coordinates if missing
            if not listing.latitude and 'latitude' in data:
                listing.latitude = data['latitude']
                listing.longitude = data['longitude']
                listing.save()
                print(f"Updated coordinates for {listing.title}")

if __name__ == '__main__':
    create_listings()
