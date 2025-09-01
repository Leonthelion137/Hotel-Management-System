from django.db import models
from django.conf import settings
from datetime import timedelta

class Room(models.Model):
    ROOM_TYPES = (
        ('normal', 'Normal'),
        ('elite', 'Elite'),
        ('deluxe', 'Deluxe'),
    )

    name = models.CharField(max_length=100, unique=True)
    is_booked = models.BooleanField(default=False)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPES)
    description = models.TextField(blank=True)
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    is_active = models.BooleanField(default=True)

    image = models.ImageField(upload_to='rooms/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.room_type})"

class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'role': 'customer'})
    image = models.ImageField(upload_to='rooms/', blank=True, null=True)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    guests = models.PositiveIntegerField(default=1)  # ✅ optional
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return f"{self.customer.username} booked {self.room.name} from {self.check_in} to {self.check_out}"

    def cleaning_buffer_end(self):
        return self.check_out + timedelta(hours=3)