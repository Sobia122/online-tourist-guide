from django.urls import path
from . import views

# For example, if you want a list of reviews:
urlpatterns = [
    path('', views.review_list, name='review_list'),
]
