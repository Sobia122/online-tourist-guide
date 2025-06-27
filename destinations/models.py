from django.db import models
from django.conf import settings

SEASONS = [
    ('Winter', 'Winter'),
    ('Spring', 'Spring'),
    ('Summer', 'Summer'),
    ('Autumn', 'Autumn'),
]

TRAVEL_TYPES = [
    ('Adventure', 'Adventure'),
    ('Leisure', 'Leisure'),
    ('Cultural', 'Cultural'),
    ('Nature', 'Nature'),
    ('Family', 'Family'),
    ('Romantic', 'Romantic'),
]

class Destination(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    season = models.CharField(max_length=10, choices=SEASONS)
    travel_type = models.CharField(max_length=100, choices=TRAVEL_TYPES, blank=True, null=True)
    image = models.ImageField(upload_to='destinations/')
    latitude = models.FloatField()
    longitude = models.FloatField()
    featured_on_homepage = models.BooleanField(default=False, help_text="Show on homepage")

    def __str__(self):
        return self.name

    def average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():  # ✅ Correct way to check if there are any reviews
            return round(sum(review.rating for review in reviews) / reviews.count(), 1)
        return 0


class Review(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='destination_reviews')
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} rated {self.destination} {self.rating}"
