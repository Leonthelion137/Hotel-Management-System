from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
from rooms.models import Room



class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('customer', 'Customer'),
        ('worker', 'Worker'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')
    is_logged_in = models.BooleanField(default=False)
    customer_id = models.UUIDField(default=None, null=True, blank=True, unique=True)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)

    _is_staff = models.BooleanField(default=False)  # internal field

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = 'admin'
            self._is_staff = True  # ensure admin access
        super().save(*args, **kwargs)

    @property
    def is_staff(self):
        return self.role == 'admin' or self._is_staff

    @is_staff.setter
    def is_staff(self, value):
        self._is_staff = value

        
class CustomerActivity(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'customer'})
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    activity_type = models.CharField(max_length=100)
    action = models.CharField(max_length=100, default='Unknown')
    notes = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.username} - {self.activity_type} at {self.timestamp}"