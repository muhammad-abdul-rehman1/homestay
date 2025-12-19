from django import forms
from .models import Listing, Review, User

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

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    is_host = forms.BooleanField(
        required=False, 
        label="I want to host homes",
        initial=False
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'is_host']
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
            
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.is_host = self.cleaned_data.get("is_host", False)
        if commit:
            user.save()
        return user
