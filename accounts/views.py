from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.utils.timezone import now
from dateutil.parser import parse
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import CustomUser
from rooms.models import Booking
from django.utils.timezone import make_aware


User = get_user_model()

def signup_view(request):
    if request.method == 'POST':
        full_name = request.POST['full_name']
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST['role']

        if User.objects.filter(email=email).exists():
            return render(request, 'home.html', {
    'signup_error': 'User already exists!',
    'show_signup': True
})

        user = User.objects.create(
            username=full_name,  # or use a custom field
            email=email,
            password=make_password(password),
            first_name=full_name,
            role=role
        )
        return redirect('login')  # Redirect to login after signup
    return redirect('home')


from django.shortcuts import render, redirect

def worker_dashboard_view(request):
    if not request.user.is_authenticated or request.user.role != 'worker':
        return redirect('home')  # redirect non-workers
    return render(request, 'accounts/worker_dashboard.html')  # render worker page


def login_view(request):
    if request.method == 'POST':
        email = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            user.is_logged_in = True
            user.save()
            if user.role == 'worker':
                return redirect('worker_dashboard')
            elif user.role == 'admin':
                return redirect('admin_dashboard')
            else:
                return redirect('customer_dashboard')
        else:
            return render(request, 'home.html', {
                'login_error': 'Invalid credentials. Please try again.',
                'show_login': True
            })

    return redirect('home')


from .models import CustomerActivity

def book_room_view(request):
    if request.user.is_authenticated and request.user.role == 'customer':
        # booking logic...
        CustomerActivity.objects.create(
            customer=request.user,
            activity_type='Booked Room',
            description='Customer booked a room for 2 nights.'
        )
        return redirect('booking_confirmation')

@login_required
def customer_dashboard_view(request):
    bookings = Booking.objects.filter(customer=request.user).select_related('room')

    return render(request, 'accounts/customer_dashboard.html', {
        'user': request.user,
        'bookings': bookings
    })


@login_required
def customer_dashboard_view(request):
    bookings = Booking.objects.filter(customer=request.user).select_related('room').order_by('-check_in')
    modal_open = False
    modal_error = None
    booking_id = None

    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        new_check_in_raw = request.POST.get('new_check_in')
        new_check_out_raw = request.POST.get('new_check_out')

        try:
            new_check_in = make_aware(parse(new_check_in_raw))
            new_check_out = make_aware(parse(new_check_out_raw))
        except Exception:
            modal_open = True
            modal_error = "Invalid date format."
            return render(request, 'accounts/customer_dashboard.html', {
                'bookings': bookings,
                'modal_open': modal_open,
                'modal_error': modal_error,
                'booking_id': booking_id
            })


        booking = get_object_or_404(Booking, id=booking_id)

        if new_check_in < now() or new_check_out < now():
            modal_open = True
            modal_error = "You can't book or modify bookings in the past."
            return render(request, 'accounts/customer_dashboard.html', {
                'bookings': bookings,
                'modal_open': modal_open,
                'modal_error': modal_error,
                'booking_id': booking_id
            })        

        conflicts = Booking.objects.filter(
            room=booking.room,
            check_out__gt=new_check_in,
            check_in__lt=new_check_out
        ).exclude(id=booking.id)

        if conflicts.exists():
            modal_open = True
            modal_error = "This time slot is already booked for this room."
        else:
            booking.check_in = new_check_in
            booking.check_out = new_check_out
            booking.save()
            messages.success(request, "Booking time updated successfully.")
            return redirect('customer_dashboard')

    return render(request, 'accounts/customer_dashboard.html', {
        'bookings': bookings,
        'modal_open': modal_open,
        'modal_error': modal_error,
        'booking_id': booking_id
    })

from menu.models import FoodOrder

@login_required
def customer_dashboard_view(request):
    bookings = Booking.objects.filter(customer=request.user).select_related('room').order_by('-check_in')
    food_orders = FoodOrder.objects.filter(customer=request.user).select_related('menu_item').order_by('-ordered_at')

    return render(request, 'accounts/customer_dashboard.html', {
        'bookings': bookings,
        'food_orders': food_orders,
        # other context variables...
    })


from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def worker_dashboard_view(request):
    return render(request, 'accounts/worker_dashboard.html')