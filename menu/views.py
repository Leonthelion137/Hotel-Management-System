from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from .models import Menu  # your model name is lowercase, but conventionally it should be uppercase
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Menu, FoodOrder
import json
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

def get_menu_items(request):
    # Convert QuerySet → list of dictionaries
    items = list(Menu.objects.values())
    return JsonResponse({
        "is_logged_in": request.user.is_authenticated,
        "items": items
    })



@csrf_exempt
def place_order(request):
    if request.method == 'POST' and request.user.is_authenticated:
        data = json.loads(request.body)
        item_id = data.get('item_id')
        quantity = data.get('quantity', 1)

        try:
            item = Menu.objects.get(id=item_id)
            FoodOrder.objects.create(customer=request.user, menu_item=item, quantity=quantity)
            return JsonResponse({'status': 'success'})
        except Menu.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Item not found'}, status=404)
    return JsonResponse({'status': 'unauthorized'}, status=401)



@login_required
def confirm_food_delivery(request, order_id):
    order = get_object_or_404(FoodOrder, id=order_id, customer=request.user)
    order.customer_confirmed = True
    order.save()
    return redirect('customer_dashboard')

@login_required
def customer_dashboard(request):
    food_orders = FoodOrder.objects.filter(
        customer=request.user
    ).select_related('menu_item').order_by('-ordered_at')

    return render(request, 'accounts/customer_dashboard.html', {
        'food_orders': food_orders
    })