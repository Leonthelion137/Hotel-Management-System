from django.urls import path
from . import views

urlpatterns = [
    path('api/menu-items/', views.get_menu_items, name='get_menu_items'),
    path('api/place-order/', views.place_order, name='place_order'),
    path('confirm-delivery/<int:order_id>/', views.confirm_food_delivery, name='confirm_food_delivery'),
]
