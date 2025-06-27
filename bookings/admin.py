from django.contrib import admin
from .models import TourBooking

@admin.register(TourBooking)
class TourBookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'destination', 'booking_date', 'persons', 'get_category', 'status', 'is_paid', 'payment_reference', 'payment_date')
    list_filter = ('booking_date', 'category', 'destination', 'status', 'is_paid')
    search_fields = ('name', 'email', 'destination__name')

    def get_category(self, obj):
        return dict(TourBooking.CATEGORY_CHOICES).get(obj.category, 'Unknown')
    get_category.short_description = 'Category'
