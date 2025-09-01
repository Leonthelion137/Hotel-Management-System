from django.urls import path
from . import views
from .views import room_data_api, api_book_room, customer_dashboard1


urlpatterns = [
    path('api/book/', views.api_book_room, name='api_book_room'),
    path('dashboard/', views.customer_dashboard1, name='customer_dashboard1'),
    path('api/rooms/', views.room_data_api, name='room_data_api'),
    path('delete-booking/<int:booking_id>/', views.delete_booking, name='delete_booking'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),


]