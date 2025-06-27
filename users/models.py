from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings  # To reference AUTH_USER_MODEL


class CustomUser(AbstractUser):
    """
    We keep 'username' for admin/staff usage, but for normal user login
    we'll rely on 'mobile_number' in a custom auth backend.
    """
    mobile_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    nationality = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    postal_address = models.TextField(blank=True, null=True)
    preferred_season = models.CharField(max_length=20, blank=True, null=True)
    preferred_travel_type = models.CharField(max_length=50, blank=True, null=True)
    age_range = models.CharField(max_length=20, blank=True, null=True)
    budget_range = models.CharField(max_length=50, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    

    def __str__(self):
        return self.username  # staff uses username in admin

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('tip_approved', 'Tip Approved'),
        ('tip_rejected', 'Tip Rejected'),
        ('new_activity', 'New Activity Added'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.message}"
