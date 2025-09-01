from django.contrib import admin
from menu.models import Menu

class MenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'desc', 'category', 'img', 'price')

admin.site.register(Menu, MenuAdmin)

from django.contrib import admin
from .models import Menu, FoodOrder

@admin.register(FoodOrder)
class FoodOrderAdmin(admin.ModelAdmin):
    list_display = (
        'menu_item_name',
        'customer_username',
        'quantity',
        'ordered_at',
        'is_delivered',
        'customer_confirmed',
        'worker_confirmed',
    )
    list_filter = ('is_delivered', 'customer_confirmed', 'worker_confirmed')
    search_fields = ('menu_item__name', 'customer__username')

    def menu_item_name(self, obj):
        return obj.menu_item.name
    menu_item_name.short_description = 'Menu Item'

    def customer_username(self, obj):
        return obj.customer.username
    customer_username.short_description = 'Customer'