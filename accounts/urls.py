from django.urls import path
from .views import signup_view, login_view 
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('dashboard/', views.customer_dashboard_view, name='customer_dashboard'),
    path('customer/', views.customer_dashboard_view, name='accounts_customer_dashboard'),
    path('worker/dashboard/', views.worker_dashboard_view, name='accounts_worker_dashboard'),
    
]
