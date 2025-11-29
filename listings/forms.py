from django import forms
from .models import Listing, Review

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = [
            'title', 'price_per_night', 'room_type', 'country', 'city', 
            'category', 'description', 'image', 
            'available_from', 'available_until', 'latitude', 'longitude'
        ]
        widgets = {
            'available_from': forms.DateInput(attrs={'type': 'date'}),
            'available_until': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3}),
        }
