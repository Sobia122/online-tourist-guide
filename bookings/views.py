# bookings/views.py
from django.shortcuts import render

def booking_dashboard(request):
    return render(request, 'bookings/dashboard.html')  # or any other template
