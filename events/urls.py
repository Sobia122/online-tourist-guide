from django.urls import path
from . import views
from .views import calendar_events_json

urlpatterns = [
  
    path('calendar-events/', calendar_events_json, name='calendar_events_json'),

]
