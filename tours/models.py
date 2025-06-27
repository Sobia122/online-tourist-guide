from django.db import models
from django.conf import settings
from destinations.models import Destination

class SavedTrip(models.Model):
    CATEGORY_CHOICES = [
        ('Adventure', 'Adventure'),
        ('Relaxation', 'Relaxation'),
        ('Cultural', 'Cultural'),
        ('Romantic', 'Romantic'),
        ('Family', 'Family'),
        ('Other', 'Other'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    travel_date_from = models.DateField()
    travel_date_to = models.DateField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Adventure')  # ✅ Added
    accommodation = models.CharField(max_length=255, blank=True, null=True)
    activities = models.TextField(blank=True, null=True)
    favorite = models.BooleanField(default=False)
    shared = models.BooleanField(default=False, help_text="Make this trip public")

    def __str__(self):
        return f"{self.user.username} trip to {self.destination.name}"
