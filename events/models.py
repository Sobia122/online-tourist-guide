from django.db import models
from destinations.models import Destination

class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.destination and not self.destination.season:
            month = self.start_date.month
            if month in [12, 1, 2]:
                self.destination.season = 'Winter'
            elif month in [3, 4, 5]:
                self.destination.season = 'Spring'
            elif month in [6, 7, 8]:
                self.destination.season = 'Summer'
            else:
                self.destination.season = 'Autumn'
            self.destination.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

