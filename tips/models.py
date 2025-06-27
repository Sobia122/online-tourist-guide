from django.db import models
from django.conf import settings
from users.models import Notification

class TravelTip(models.Model):
    SEASON_CHOICES = [
        ('Autumn', 'Autumn'),
        ('Spring', 'Spring'),
        ('Summer', 'Summer'),
        ('Winter', 'Winter')
    ]

    TIP_TYPE_CHOICES = [
        ('Safety', 'Safety'),
        ('Budget', 'Budget'),
        ('Packing', 'Packing'),
        ('General', 'General'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    season = models.CharField(max_length=20, choices=SEASON_CHOICES)
    tip_type = models.CharField(max_length=50, choices=TIP_TYPE_CHOICES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        old_approved = None

        if not is_new:
            old = TravelTip.objects.get(pk=self.pk)
            old_approved = old.approved

        super().save(*args, **kwargs)

        if (is_new and self.approved) or (not is_new and not old_approved and self.approved):
            if self.user:
                Notification.objects.create(
                    user=self.user,
                    message=f"✅ Your travel tip '{self.title}' was approved!",
                    notification_type='tip_approved'
                )
