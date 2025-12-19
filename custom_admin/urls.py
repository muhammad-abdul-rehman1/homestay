from django.urls import path
from . import views

app_name = 'custom_admin'

urlpatterns = [
    path('', views.AdminDashboardView.as_view(), name='dashboard'),
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/<int:pk>/action/<str:action>/', views.UserActionView.as_view(), name='user_action'),
    path('listings/', views.ListingListView.as_view(), name='listing_list'),
    path('listings/<int:pk>/action/<str:action>/', views.ListingActionView.as_view(), name='listing_action'),
    path('bookings/', views.BookingListView.as_view(), name='booking_list'),
    path('bookings/<int:pk>/cancel/', views.BookingCancelView.as_view(), name='booking_cancel'),
    path('payments/', views.PaymentListView.as_view(), name='payment_list'),
]
