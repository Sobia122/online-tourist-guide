from django import forms
from .models import Photo, PhotoInteraction

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image', 'caption', 'destination', 'tour_type']

class CommentForm(forms.ModelForm):
    class Meta:
        model = PhotoInteraction
        fields = ['comment']
