# admin.py

from django.contrib import admin
from .models import Destination, Review
from django.db.models import Count

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ['name', 'season', 'latitude', 'longitude', 'featured_on_homepage', 'booking_count']
    list_editable = ['featured_on_homepage']  # ✅ Editable from list
    search_fields = ['name']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(booking_count=Count('tourbooking'))

    def booking_count(self, obj):
        return obj.booking_count
    booking_count.short_description = 'Total Bookings'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['destination', 'user', 'rating', 'created_at']
    search_fields = ['destination__name', 'user__username', 'comment']
