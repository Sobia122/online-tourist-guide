from django.urls import path
from . import views

app_name = 'destinations'  # ✅ Required for namespacing

urlpatterns = [
    path('<int:destination_id>/', views.destination_detail, name='destination_detail'),
    path('like_photo/<int:photo_id>/', views.like_photo, name='like_photo'),
]
