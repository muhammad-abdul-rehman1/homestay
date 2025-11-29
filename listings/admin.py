from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Listing, Booking

admin.site.register(User, UserAdmin)
admin.site.register(Listing)
admin.site.register(Booking)
