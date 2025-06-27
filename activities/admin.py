from django.contrib import admin
from .models import Activity

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'season', 'activity_type', 'get_destination', 'image')  # Add image to display
    fields = ('title', 'description', 'season', 'activity_type', 'destination', 'image')  # Ensure image is included

    def get_destination(self, obj):
        return obj.destination.name if obj.destination else "No Destination"

    get_destination.short_description = "Destination"


