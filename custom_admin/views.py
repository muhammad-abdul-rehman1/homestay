from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
from django.db.models import Sum, Count
from listings.models import Listing, Booking

User = get_user_model()

class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

class AdminDashboardView(AdminRequiredMixin, TemplateView):
    template_name = 'custom_admin/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_users'] = User.objects.count()
        context['total_hosts'] = User.objects.filter(is_host=True).count()
        context['total_guests'] = User.objects.filter(is_host=False, is_superuser=False).count()
        context['total_listings'] = Listing.objects.count()
        context['total_bookings'] = Booking.objects.count()
        context['total_revenue'] = Booking.objects.filter(is_paid=True).aggregate(Sum('total_price'))['total_price__sum'] or 0
        
        # Recent activity
        context['recent_listings'] = Listing.objects.order_by('-created_at')[:5]
        context['recent_bookings'] = Booking.objects.order_by('-created_at')[:5]
        return context

class UserListView(AdminRequiredMixin, ListView):
    model = User
    template_name = 'custom_admin/user_list.html'
    context_object_name = 'users'
    paginate_by = 20

    def get_queryset(self):
        role = self.request.GET.get('role')
        queryset = User.objects.all().order_by('-date_joined')
        if role == 'admin':
            queryset = queryset.filter(is_superuser=True)
        elif role == 'host':
            queryset = queryset.filter(is_host=True)
        elif role == 'guest':
            queryset = queryset.filter(is_host=False, is_superuser=False)
        return queryset

class UserActionView(AdminRequiredMixin, View):
    def post(self, request, pk, action):
        user = get_object_or_404(User, pk=pk)
        # Prevent self-deletion
        if action == 'delete' and user == request.user:
            # Should add message
            return redirect('custom_admin:user_list')
        
        if action == 'delete':
            user.delete()
        elif action == 'activate':
            user.is_active = True
            user.save()
        elif action == 'deactivate':
            user.is_active = False
            user.save()
            
        return redirect('custom_admin:user_list')

class ListingListView(AdminRequiredMixin, ListView):
    model = Listing
    template_name = 'custom_admin/listing_list.html'
    context_object_name = 'listings'
    paginate_by = 20

    def get_queryset(self):
        status = self.request.GET.get('status')
        queryset = Listing.objects.all().select_related('host').order_by('-created_at')
        if status:
            queryset = queryset.filter(status=status)
        return queryset

class ListingActionView(AdminRequiredMixin, View):
    def post(self, request, pk, action):
        listing = get_object_or_404(Listing, pk=pk)
        
        if action == 'approve':
            listing.status = 'approved'
            listing.save()
        elif action == 'reject':
            listing.status = 'rejected'
            listing.save()
        elif action == 'delete':
            listing.delete()
            
        return redirect('custom_admin:listing_list')

class BookingListView(AdminRequiredMixin, ListView):
    model = Booking
    template_name = 'custom_admin/booking_list.html'
    context_object_name = 'bookings'
    paginate_by = 20

    def get_queryset(self):
        queryset = Booking.objects.all().select_related('listing', 'guest').order_by('-created_at')
        return queryset

class BookingCancelView(AdminRequiredMixin, View):
    def post(self, request, pk):
        booking = get_object_or_404(Booking, pk=pk)
        booking.delete() # Or set status to cancelled
        return redirect('custom_admin:booking_list')

class PaymentListView(AdminRequiredMixin, ListView):
    model = Booking
    template_name = 'custom_admin/payment_list.html'
    context_object_name = 'payments'
    paginate_by = 20

    def get_queryset(self):
        return Booking.objects.filter(is_paid=True).select_related('guest', 'listing').order_by('-created_at')
