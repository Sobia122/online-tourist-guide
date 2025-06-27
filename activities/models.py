from django.db import models
from django.conf import settings
from django.utils import timezone
from users.models import Notification, CustomUser  # ✅ Import for notifications

class Activity(models.Model):
    SEASON_CHOICES = [
        ('Winter', 'Winter'),
        ('Spring', 'Spring'),
        ('Summer', 'Summer'),
        ('Autumn', 'Autumn'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    season = models.CharField(max_length=10, choices=SEASON_CHOICES)
    activity_type = models.CharField(max_length=50)
    destination = models.ForeignKey('destinations.Destination', on_delete=models.CASCADE, related_name='activities')
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='activities/', null=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            # ✅ Create a notification for every user
            for user in CustomUser.objects.all():
                Notification.objects.create(
                    user=user,
                    message=f"🎉 New activity '{self.title}' added! Check it out.",
                    notification_type='new_activity'
                )


