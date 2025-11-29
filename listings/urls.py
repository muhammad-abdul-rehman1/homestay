from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('listing/<int:id>/', views.listing_detail, name='listing_detail'),
    path('become-host/', views.become_host, name='become_host'),
    path('create-listing/', views.create_listing, name='create_listing'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('my-listings/', views.my_listings, name='my_listings'),
    path('listing/<int:id>/edit/', views.edit_listing, name='edit_listing'),
    path('listing/<int:id>/delete/', views.delete_listing, name='delete_listing'),
    path('listing/<int:id>/review/', views.add_review, name='add_review'),
    path('listing/<int:listing_id>/book/', views.checkout, name='checkout'),
    path('booking/<int:booking_id>/confirmation/', views.booking_confirmation, name='booking_confirmation'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('booking/create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('booking/process-jazzcash/', views.process_jazzcash_payment, name='process_jazzcash_payment'),
    path('booking/success/stripe/', views.payment_success, name='payment_success'),
    path('webhook/stripe/', views.stripe_webhook, name='stripe_webhook'),
    path('profile/', views.profile_view, name='profile'),
]
