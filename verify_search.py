import os
import django
from django.db.models import Q

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from listings.models import Listing

query = 'cozy'
listings = Listing.objects.filter(
    Q(title__icontains=query) | 
    Q(city__icontains=query) |
    Q(country__icontains=query) |
    Q(description__icontains=query)
)

print(f"Search results for '{query}':")
for listing in listings:
    print(f"- {listing.title}")
    if query in listing.description.lower():
        print(f"  (Matched description)")
    if query in listing.title.lower():
        print(f"  (Matched title)")
    if listing.city and query in listing.city.lower():
        print(f"  (Matched city)")
    if query in listing.country.lower():
        print(f"  (Matched country)")

print("-" * 20)
print("All Listings:")
for listing in Listing.objects.all():
    print(f"- {listing.title}")
