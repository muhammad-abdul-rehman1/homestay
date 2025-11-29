from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_host = models.BooleanField(default=False)

class Listing(models.Model):
    ROOM_TYPE_CHOICES = (
        ('entire_place', 'Entire Place'),
        ('private_room', 'Private Room'),
        ('shared_room', 'Shared Room'),
    )

    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    title = models.CharField(max_length=255)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='listings/')
    category = models.CharField(max_length=50, default='beach')
    description = models.TextField(blank=True)
    available_from = models.DateField(null=True, blank=True)
    available_until = models.DateField(null=True, blank=True)
    amenities = models.JSONField(default=dict)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.title

    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            return sum([r.rating for r in reviews]) / len(reviews)
        return 0

class Review(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s review for {self.listing.title}"

class Booking(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bookings')
    guest = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    check_in = models.DateField()
    check_out = models.DateField()
    num_guests = models.IntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Payment fields
    PAYMENT_METHOD_CHOICES = (
        ('stripe', 'Stripe'),
        ('jazzcash', 'JazzCash'),
    )
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, blank=True, null=True)
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    status = models.CharField(max_length=20, default='pending_payment')

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.check_in and self.check_out and self.check_in >= self.check_out:
            raise ValidationError("Check-out date must be after check-in date.")
            
        # Check for overlapping bookings for the same listing
        overlapping_bookings = Booking.objects.filter(
            listing=self.listing,
            check_in__lt=self.check_out,
            check_out__gt=self.check_in
        ).exclude(id=self.id)
        
        if overlapping_bookings.exists():
            raise ValidationError("This listing is already booked for the selected dates.")

        # Check for overlapping bookings for the same guest (across any listing)
        guest_overlapping_bookings = Booking.objects.filter(
            guest=self.guest,
            check_in__lt=self.check_out,
            check_out__gt=self.check_in
        ).exclude(id=self.id)

        if guest_overlapping_bookings.exists():
            raise ValidationError("You already have a booking for these dates.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking for {self.listing.title} by {self.guest.username}"
