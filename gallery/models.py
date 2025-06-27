from django.db import models
from django.contrib.auth import get_user_model
from destinations.models import Destination  # Update based on your project structure

User = get_user_model()

class Photo(models.Model):
    image = models.ImageField(upload_to='photos/')
    caption = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, null=True, blank=True)
    tour_type = models.CharField(max_length=50, choices=[
        ('Ocean', 'Ocean'),
        ('Summer', 'Summer'),
        ('Sport', 'Sport')
    ], blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class PhotoInteraction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='interactions')
    liked = models.BooleanField(default=False)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'photo')  # ensures one interaction per user-photo pair

    def __str__(self):
        return f"{self.user.username} - {self.photo.caption} - Liked: {self.liked}"
