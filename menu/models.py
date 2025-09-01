from django.db import models
from django.contrib.auth import get_user_model


class Menu(models.Model): 
    name = models.CharField(max_length=255)
    desc = models.TextField()
    category = models.CharField(max_length=50)
    img = models.URLField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name
    

User = get_user_model()

class FoodOrder(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_at = models.DateTimeField(auto_now_add=True)
    is_delivered = models.BooleanField(default=False)
    customer_confirmed = models.BooleanField(default=False)
    worker_confirmed = models.BooleanField(default=False)

    def is_fully_confirmed(self):
        return self.is_delivered and self.customer_confirmed and self.worker_confirmed