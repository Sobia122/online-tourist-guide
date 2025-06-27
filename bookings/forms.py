from django import forms
from .models import TourBooking

class TourBookingForm(forms.ModelForm):
    class Meta:
        model = TourBooking
        fields = ['name', 'email', 'booking_date', 'destination', 'persons', 'category', 'special_request', 'is_paid', 'payment_reference', 'payment_date']
        widgets = {
            'booking_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'payment_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
