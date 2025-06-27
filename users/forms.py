from django import forms
from django.contrib.auth.forms import UserCreationForm
from captcha.fields import CaptchaField
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    """
    Signup form with:
      - first_name, last_name, nationality, city, postal_address,
      - mobile_number, email, password1, password2,
      - personal preferences (season, type, age, budget),
      - captcha
    """
    captcha = CaptchaField()

    class Meta:
        model = CustomUser
        fields = [
            'username',        # staff user can have a username
            'email',
            'first_name',
            'last_name',
            'mobile_number',
            'nationality',
            'city',
            'postal_address',
            'preferred_season',
            'preferred_travel_type',
            'age_range',
            'budget_range',
            'profile_picture',
            'password1',
            'password2'
        ]

class CustomUserForm(forms.ModelForm):
    """
    For updating user profile after login.
    """
    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'mobile_number',
            'nationality',
            'city',
            'postal_address',
            'preferred_season',
            'preferred_travel_type',
            'age_range',
            'budget_range',
            'profile_picture'
        ]
