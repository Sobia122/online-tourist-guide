from django.db import models
from users.models import CustomUser
from destinations.models import Destination

class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)