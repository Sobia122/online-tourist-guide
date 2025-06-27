from django import forms
from .models import TravelTip

class TravelTipForm(forms.ModelForm):
    class Meta:
        model = TravelTip
        fields = ['title', 'content', 'season', 'tip_type']
