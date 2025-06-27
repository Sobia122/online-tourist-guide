# bookings/urls.py
from django.urls import path
from . import views  # Make sure views.py exists and has the required functions

urlpatterns = [
    path('', views.booking_dashboard, name='booking_dashboard'),  # Example path
    # Add other paths as needed
]
