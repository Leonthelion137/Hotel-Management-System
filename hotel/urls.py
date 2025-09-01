"""
URL configuration for hotel project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from hotel import views
from django.urls import path, include
from accounts.views import worker_dashboard_view
from .views import customer_dashboard_view
from django.conf import settings
from django.conf.urls.static import static
from hotel.views import my_bookings
from rooms.models import Booking

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homePage,name='home'),
    path('about-us/',views.aboutus,name='about_us'),
    path('menu/',views.menu,name='menu'),
    path('bookroom/',views.bookroom,name='bookroom'),
    path('', include('menu.urls')), 
    path('accounts/', include('accounts.urls')),
    path('worker/', worker_dashboard_view, name='worker_dashboard'),
    
    path('rooms/', include('rooms.urls')),
    path('my-bookings/', my_bookings, name='my_bookings'),
    

    


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


