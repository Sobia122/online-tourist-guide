from django.shortcuts import render
from .models import Review  # Make sure you have a Review model

def review_list(request):
    reviews = Review.objects.all()
    return render(request, 'reviews/list.html', {'reviews': reviews})
