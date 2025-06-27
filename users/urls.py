from django.urls import path, include
from django.contrib.auth.views import LogoutView
from .views import mark_notification_as_read
from .views import analytics_dashboard

from .views import dashboard

from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('analytics/', analytics_dashboard, name='analytics_dashboard'),

    # Include captcha URLs for django-simple-captcha:
    path('captcha/', include('captcha.urls')),
    path('dashboard/', dashboard, name='dashboard'),
    path('delete-trip/<int:trip_id>/', views.delete_trip, name='delete_trip'),  # 👈 Add this

    path('login/', views.user_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile-update/', views.profile_update, name='profile_update'),
    path('logout/', views.custom_logout, name='logout'),
    path('notifications/', views.notification_list, name='notification_list'),
    path('notifications/<int:notification_id>/read/', views.mark_notification_as_read, name='mark_notification_as_read'),

]
