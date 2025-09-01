from django.http import JsonResponse
from django.shortcuts import render , redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Room, Booking
from accounts.models import CustomUser, CustomerActivity
from .utils import is_room_available  # if used elsewhere
import json
from datetime import datetime
from dateutil.parser import parse
from django.utils import timezone
from django.contrib import messages


def room_data_api(request):
    rooms = Room.objects.filter(is_active=True)
    data = [
        {
            'name': room.name,
            'room_type': room.room_type,
            'price': f"${room.price_per_night}/night",
            'desc': room.description,
            'img': '/static/images/default-room.jpg'  # Replace with actual image field if available
        }
        for room in rooms
    ]
    return JsonResponse(data, safe=False)


# 🛡️ API endpoint to book a room
# Frontend should send CSRF token manually if needed
@csrf_exempt
def api_book_room(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            room_name = data.get('roomName')
            check_in = data.get('arrivalDate')
            check_out = data.get('departureDate')
            guests = data.get('guests', 1)

            customer = request.user if request.user.is_authenticated else None
            if not customer:
                return JsonResponse({'error': 'Login required'}, status=403)

            try:
                room = Room.objects.get(name=room_name)
            except Room.DoesNotExist:
                return JsonResponse({'error': 'Room not found'}, status=404)

            try:
                check_in_date = parse(str(check_in)).date()
                check_out_date = parse(str(check_out)).date()
            except Exception:
                return JsonResponse({'error': 'Invalid date format'}, status=400)

            # ✅ Prevent double booking
            conflict = Booking.objects.filter(
                room=room,
                check_in__lt=check_out_date,
                check_out__gt=check_in_date
            ).exists()

            if conflict:
                return JsonResponse({'error': 'Room is already booked for those dates.'}, status=400)

            # ✅ Create booking
            booking = Booking.objects.create(
                room=room,
                customer=customer,
                check_in=check_in_date,
                check_out=check_out_date,
                guests=guests
            )


            room.is_booked = True
            room.save()

            CustomerActivity.objects.create(
                customer=customer,
                room=room,
                action="Booked",
                notes=f"Check-in: {check_in_date}, Check-out: {check_out_date}"
            )


            return JsonResponse({
            'message': 'Booking successful',
            'booking_id': booking.id,
            'room': room.name,
            'check_in': str(check_in_date),
            'check_out': str(check_out_date)
})


        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)




# 👤 Dashboard for logged-in customers to view their bookings
@login_required
def customer_dashboard1(request):
    bookings = Booking.objects.filter(customer=request.user).order_by('-check_in')
    return render(request, 'rooms/dashboard.html', {'bookings': bookings})\
    


def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.delete()
    return redirect('my_bookings')

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(customer=request.user).order_by('-check_in')
    modal_open = False
    modal_error = None
    booking_id = None

    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        new_check_in_raw = request.POST.get('new_check_in')
        new_check_out_raw = request.POST.get('new_check_out')

        try:
            new_check_in = parse(new_check_in_raw)
            new_check_out = parse(new_check_out_raw)
        except Exception:
            modal_open = True
            modal_error = "Invalid date format."
            return render(request, 'hotel/my_bookings.html', {
                'bookings': bookings,
                'modal_open': modal_open,
                'modal_error': modal_error,
                'booking_id': booking_id
            })

        booking = get_object_or_404(Booking, id=booking_id)

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
            return redirect('my_bookings')

    return render(request, 'hotel/my_bookings.html', {
        'bookings': bookings,
        'modal_open': modal_open,
        'modal_error': modal_error,
        'booking_id': booking_id
    })





# 🧹 Placeholder for future worker dashboard
# @login_required
# def worker_dashboard(request):
#     # Logic for cleaning schedules or room status
#     pass


# 🏨 Optional: Room listing view
# def room_list(request):
#     rooms = Room.objects.all()
#     return render(request, 'rooms/room_list.html', {'rooms': rooms})