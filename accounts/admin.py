from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, CustomerActivity
from menu.models import FoodOrder
from django.contrib.auth import get_user_model


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'role', 'phone', 'address']
    list_filter = ['role', 'is_superuser']  # Removed 'is_staff'
    search_fields = ['username', 'email']
    ordering = ['email']

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'phone', 'address', 'profile_image')}),
    )

    def has_module_permission(self, request):
        return request.user.is_active and request.user.role == 'admin' 
    

admin.site.register(CustomUser, CustomUserAdmin)




