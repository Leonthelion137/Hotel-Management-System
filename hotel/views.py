from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rooms.models import Booking


def homePage(request):
    return render(request,"home.html")

def aboutus(request):
    return render(request,"aboutus.html")
def menu(request):
    return render(request,"menu.html")
def bookroom(request):
    return render(request,"bookroom.html")

@login_required
def customer_dashboard_view(request):
    return render(request, 'accounts/customer_dashboard.html')

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(customer=request.user).select_related('room')
    return render(request, 'room/dashboard.html', {'bookings': bookings})


from rooms.models import Booking

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(customer=request.user)
    print("Logged-in user:", request.user)
    print("Bookings found:", bookings.count())
    for b in bookings:
        print("Room:", b.room, "Check-in:", b.check_in)
    return render(request, 'accounts/customer_dashboard.html',  {'bookings': bookings})
