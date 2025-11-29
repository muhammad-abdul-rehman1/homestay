from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Listing, User, Booking, Review
from .forms import ListingForm, ReviewForm
from datetime import datetime
import stripe
import json
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from django.db.models import Q

def home(request):
    query = request.GET.get('search')
    category = request.GET.get('category')
    
    listings = Listing.objects.all()
    
    if query:
        listings = listings.filter(
            Q(title__icontains=query) | 
            Q(city__icontains=query) |
            Q(country__icontains=query)
        )
        
    if category:
        listings = listings.filter(category=category)
        
    return render(request, 'listings/home.html', {'listings': listings})

def listing_detail(request, id):
    listing = get_object_or_404(Listing, id=id)
    # Format room_type for display
    room_type_display = listing.room_type.replace('_', ' ').title()
    # Format host name for display
    host_display_name = listing.host.username.title()
    # Format dates for display
    available_from_display = listing.available_from.strftime("%B %d, %Y") if listing.available_from else None
    available_until_display = listing.available_until.strftime("%B %d, %Y") if listing.available_until else None
    return render(request, 'listings/listing_detail.html', {
        'listing': listing,
        'room_type_display': room_type_display,
        'host_display_name': host_display_name,
        'available_from_display': available_from_display,
        'available_until_display': available_until_display
    })

def become_host(request):
    return render(request, 'listings/become_host.html')

@login_required
def create_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.host = request.user
            listing.save()
            messages.success(request, f'Your listing "{listing.title}" has been created successfully!')
            return redirect('home')
    else:
        form = ListingForm()
    
    return render(request, 'listings/create_listing.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Check if user already exists
        if User.objects.filter(email=email).exists():
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': 'Email already registered.'}, status=400)
            messages.error(request, 'Email already registered.')
            return redirect('home')
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        # Log the user in
        login(request, user)
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
            
        messages.success(request, f'Welcome to HomeStay, {username}!')
        return redirect('home')
    
    return redirect('home')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Try to find user by email
        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
            
            if user is not None:
                login(request, user)
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'success': True})
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('home')
            else:
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'error': 'Invalid email or password.'}, status=400)
                messages.error(request, 'Invalid email or password.')
        except User.DoesNotExist:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': 'Invalid email or password.'}, status=400)
            messages.error(request, 'Invalid email or password.')
        
        return redirect('home')
    
    return redirect('home')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

@login_required
def my_listings(request):
    listings = Listing.objects.filter(host=request.user).order_by('-id')
    return render(request, 'listings/my_listings.html', {'listings': listings})

@login_required
def edit_listing(request, id):
    listing = get_object_or_404(Listing, id=id, host=request.user)
    
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your listing "{listing.title}" has been updated successfully!')
            return redirect('my_listings')
    else:
        form = ListingForm(instance=listing)
    
    return render(request, 'listings/edit_listing.html', {'form': form, 'listing': listing})

@login_required
def delete_listing(request, id):
    listing = get_object_or_404(Listing, id=id, host=request.user)
    
    if request.method == 'POST':
        title = listing.title
        listing.delete()
        messages.success(request, f'Listing "{title}" has been deleted successfully!')
        return redirect('my_listings')
    
    return render(request, 'listings/delete_listing.html', {'listing': listing})

@login_required
def checkout(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    
    # Prevent users from booking their own listings
    if request.user == listing.host:
        messages.error(request, 'You cannot book your own listing.')
        return redirect('listing_detail', id=listing_id)
    
    if request.method == 'POST':
        check_in_str = request.POST.get('check_in')
        check_out_str = request.POST.get('check_out')
        num_guests = int(request.POST.get('num_guests'))
        
        # Parse dates
        check_in = datetime.strptime(check_in_str, '%Y-%m-%d').date()
        check_out = datetime.strptime(check_out_str, '%Y-%m-%d').date()
        
        # Validate dates
        if check_out <= check_in:
            messages.error(request, 'Check-out date must be after check-in date.')
            return redirect('listing_detail', id=listing_id)
            
        # Check for overlapping bookings
        overlapping_bookings = Booking.objects.filter(
            listing=listing,
            check_in__lt=check_out,
            check_out__gt=check_in
        ).exists()
        
        if overlapping_bookings:
            messages.error(request, 'This listing is already booked for the selected dates. Please choose different dates.')
            return redirect('listing_detail', id=listing_id)

        # Check for overlapping bookings for the same guest (across any listing)
        guest_overlapping_bookings = Booking.objects.filter(
            guest=request.user,
            check_in__lt=check_out,
            check_out__gt=check_in
        ).exists()

        if guest_overlapping_bookings:
            messages.error(request, 'You already have a booking for these dates.')
            return redirect('listing_detail', id=listing_id)
        
        # Calculate number of nights and total price
        num_nights = (check_out - check_in).days
        total_price = num_nights * listing.price_per_night
        
        # Store booking details in session
        request.session['booking_details'] = {
            'listing_id': listing.id,
            'check_in': check_in_str,
            'check_out': check_out_str,
            'num_guests': num_guests,
            'num_nights': num_nights,
            'total_price': float(total_price)
        }
        
        context = {
            'listing': listing,
            'check_in': check_in,
            'check_out': check_out,
            'num_guests': num_guests,
            'num_nights': num_nights,
            'total_price': total_price,
            'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
            'paypal_client_id': settings.PAYPAL_CLIENT_ID
        }
        
        return render(request, 'listings/checkout.html', context)
    
    return redirect('listing_detail', id=listing_id)

@login_required
def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, guest=request.user)
    num_nights = (booking.check_out - booking.check_in).days
    return render(request, 'listings/booking_confirmation.html', {
        'booking': booking,
        'num_nights': num_nights
    })

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(guest=request.user).order_by('-check_in')
    return render(request, 'listings/my_bookings.html', {'bookings': bookings})

@login_required
def create_checkout_session(request):
    if request.method == 'POST':
        booking_details = request.session.get('booking_details')
        if not booking_details:
            return JsonResponse({'error': 'No booking details found'}, status=400)
            
        listing = get_object_or_404(Listing, id=booking_details['listing_id'])
        stripe.api_key = settings.STRIPE_SECRET_KEY
        
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': f"Booking for {listing.title}",
                        },
                        'unit_amount': int(booking_details['total_price'] * 100),
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri('/booking/success/stripe/') + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=request.build_absolute_uri(f'/listing/{listing.id}/'),
                metadata={
                    'listing_id': listing.id,
                    'guest_id': request.user.id,
                    'check_in': booking_details['check_in'],
                    'check_out': booking_details['check_out'],
                    'num_guests': booking_details['num_guests'],
                    'total_price': booking_details['total_price']
                }
            )
            return JsonResponse({'id': checkout_session.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def process_jazzcash_payment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        booking_details = request.session.get('booking_details')
        
        if not booking_details:
            return JsonResponse({'error': 'No booking details found'}, status=400)
            
        listing = get_object_or_404(Listing, id=booking_details['listing_id'])
        
        # Create booking
        booking = Booking.objects.create(
            listing=listing,
            guest=request.user,
            check_in=datetime.strptime(booking_details['check_in'], '%Y-%m-%d').date(),
            check_out=datetime.strptime(booking_details['check_out'], '%Y-%m-%d').date(),
            num_guests=booking_details['num_guests'],
            total_price=booking_details['total_price'],
            payment_method='jazzcash',
            payment_id=f"JC-{datetime.now().strftime('%Y%m%d%H%M%S')}", # Simulated Transaction ID
            is_paid=True,
            status='confirmed'
        )
        
        # Clear session
        del request.session['booking_details']
        
        messages.success(request, 'Payment successful via JazzCash! Your booking is confirmed.')
        return JsonResponse({'success': True, 'booking_id': booking.id})

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return JsonResponse({'error': 'Invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return JsonResponse({'error': 'Invalid signature'}, status=400)

    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        # Retrieve metadata
        metadata = session.get('metadata', {})
        listing_id = metadata.get('listing_id')
        guest_id = metadata.get('guest_id')
        check_in_str = metadata.get('check_in')
        check_out_str = metadata.get('check_out')
        num_guests = metadata.get('num_guests')
        total_price = metadata.get('total_price')
        
        if listing_id and guest_id:
            try:
                listing = Listing.objects.get(id=listing_id)
                guest = User.objects.get(id=guest_id)
                
                Booking.objects.create(
                    listing=listing,
                    guest=guest,
                    check_in=datetime.strptime(check_in_str, '%Y-%m-%d').date(),
                    check_out=datetime.strptime(check_out_str, '%Y-%m-%d').date(),
                    num_guests=int(num_guests),
                    total_price=float(total_price),
                    payment_method='stripe',
                    payment_id=session.get('payment_intent'),
                    is_paid=True,
                    status='confirmed'
                )
            except (Listing.DoesNotExist, User.DoesNotExist, ValueError) as e:
                print(f"Error creating booking from webhook: {e}")
                return JsonResponse({'error': 'Error creating booking'}, status=500)

    return JsonResponse({'status': 'success'})

def payment_success(request):
    session_id = request.GET.get('session_id')
    if not session_id:
        messages.error(request, 'No payment session found.')
        return redirect('home')

    stripe.api_key = settings.STRIPE_SECRET_KEY
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        
        if session.payment_status == 'paid':
            # Retrieve metadata
            metadata = session.get('metadata', {})
            listing_id = metadata.get('listing_id')
            guest_id = metadata.get('guest_id')
            check_in_str = metadata.get('check_in')
            check_out_str = metadata.get('check_out')
            num_guests = metadata.get('num_guests')
            total_price = metadata.get('total_price')
            
            if listing_id and guest_id:
                listing = Listing.objects.get(id=listing_id)
                guest = User.objects.get(id=guest_id)
                
                # Check if booking already exists (to prevent duplicates from webhook)
                payment_id = session.get('payment_intent')
                if not Booking.objects.filter(payment_id=payment_id).exists():
                    booking = Booking.objects.create(
                        listing=listing,
                        guest=guest,
                        check_in=datetime.strptime(check_in_str, '%Y-%m-%d').date(),
                        check_out=datetime.strptime(check_out_str, '%Y-%m-%d').date(),
                        num_guests=int(num_guests),
                        total_price=float(total_price),
                        payment_method='stripe',
                        payment_id=payment_id,
                        is_paid=True,
                        status='confirmed'
                    )
                    messages.success(request, 'Payment successful! Your booking is confirmed.')
                    return redirect('booking_confirmation', booking_id=booking.id)
                else:
                    # If booking exists, find it and redirect
                    booking = Booking.objects.get(payment_id=payment_id)
                    return redirect('booking_confirmation', booking_id=booking.id)
                    
    except Exception as e:
        print(f"Error processing payment success: {e}")
        # Check if it's a validation error (likely overlapping booking from webhook race condition)
        if "already booked" in str(e) or "Check-out date must be after" in str(e):
            # Try to find the booking that caused the overlap (likely ours)
            try:
                metadata = session.get('metadata', {})
                listing_id = metadata.get('listing_id')
                guest_id = metadata.get('guest_id')
                check_in_str = metadata.get('check_in')
                check_out_str = metadata.get('check_out')
                
                if listing_id and guest_id and check_in_str and check_out_str:
                    existing_booking = Booking.objects.filter(
                        listing_id=listing_id,
                        guest_id=guest_id,
                        check_in=datetime.strptime(check_in_str, '%Y-%m-%d').date(),
                        check_out=datetime.strptime(check_out_str, '%Y-%m-%d').date()
                    ).first()
                    
                    if existing_booking:
                        messages.success(request, 'Payment successful! Your booking is confirmed.')
                        return redirect('booking_confirmation', booking_id=existing_booking.id)
            except Exception as inner_e:
                print(f"Error finding existing booking: {inner_e}")

        messages.error(request, f'Error processing payment: {e}')
        
    return redirect('my_bookings')

@login_required
def add_review(request, id):
    listing = get_object_or_404(Listing, id=id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            # Check if user has already reviewed this listing
            if Review.objects.filter(listing=listing, user=request.user).exists():
                messages.error(request, 'You have already reviewed this listing.')
            else:
                review = form.save(commit=False)
                review.listing = listing
                review.user = request.user
                review.save()
                messages.success(request, 'Your review has been submitted.')
    
    return redirect('listing_detail', id=id)

@login_required
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        
        if email != user.email:
            if User.objects.filter(email=email).exclude(id=user.id).exists():
                messages.error(request, 'Email already in use.')
                return redirect('profile')
            user.email = email
            
        user.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')
        
    return render(request, 'listings/profile.html', {'user': user})
