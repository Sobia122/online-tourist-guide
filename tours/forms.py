from django import forms
from .models import SavedTrip

class SavedTripForm(forms.ModelForm):
    class Meta:
        model = SavedTrip
        fields = [
           
            'destination', 'travel_date_from', 'travel_date_to',
            'category',  
            'accommodation', 'activities',
            'favorite', 'shared',
        ]
        widgets = {
            'travel_date_from': forms.DateInput(attrs={'type': 'date'}),
            'travel_date_to': forms.DateInput(attrs={'type': 'date'}),
        }
