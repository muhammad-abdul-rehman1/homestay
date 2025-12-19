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
    print(f"\nTitle: {listing.title}")
    if query in listing.description.lower():
        try:
            print(f"Description match: ...{listing.description}...")
        except UnicodeEncodeError:
            print(f"Description match: ...{listing.description.encode('utf-8')}...")
    else:
        print("Description: (No match)")
