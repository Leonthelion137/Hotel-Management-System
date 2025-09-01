from django.contrib import admin
from .models import Room, Booking

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['name','image', 'room_type', 'price_per_night', 'is_active']
    search_fields = ['name', 'room_type']
    fields = ('name', 'room_type', 'price_per_night', 'description', 'is_active', 'image')
    list_filter = ['room_type', 'is_active']
    

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['room', 'customer', 'check_in', 'check_out']
    search_fields = ['room__name', 'customer__username']
    list_filter = ['check_in', 'check_out']