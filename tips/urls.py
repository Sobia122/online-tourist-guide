from django.urls import path
from . import views
from .views import submit_tip

urlpatterns = [
    path('', views.tip_list, name='tip_list'),
    path('<int:pk>/', views.tip_detail, name='tip_detail'),
    path('new/', views.tip_create, name='tip_create'),
    path('<int:pk>/edit/', views.tip_update, name='tip_update'),
    path('<int:pk>/delete/', views.tip_delete, name='tip_delete'),
    path('submit/', submit_tip, name='submit_tip'),  # Ensure this exists
    

]
