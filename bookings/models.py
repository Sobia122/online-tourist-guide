from django.db import models
from destinations.models import Destination
from django.conf import settings

class TourBooking(models.Model):
    CATEGORY_CHOICES = [
        (1, 'Kids'),
        (2, 'Adults'),
        (3, 'Family'),
        (4, 'Group'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    booking_date = models.DateTimeField()
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    persons = models.IntegerField()
    category = models.IntegerField(choices=CATEGORY_CHOICES)
    special_request = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    # ✅ New payment tracking fields
    is_paid = models.BooleanField(default=False)
    payment_reference = models.CharField(max_length=100, blank=True, null=True)
    payment_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.destination.name} on {self.booking_date}"
