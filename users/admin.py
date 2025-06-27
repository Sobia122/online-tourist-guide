from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import CustomUser, Notification

class CustomUserAdmin(UserAdmin):
    """
    Custom admin panel for the CustomUser model.
    """
    model = CustomUser

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'mobile_number', 'profile_picture')}),
        ('Location & Contact', {'fields': ('nationality', 'city', 'postal_address')}),
        ('Preferences', {'fields': ('preferred_season', 'preferred_travel_type', 'age_range', 'budget_range')}),  
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),  
        ('Important dates', {'fields': ('last_login', 'date_joined')}),  
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'first_name', 'last_name', 'email', 'mobile_number', 
                'nationality', 'city', 'postal_address',
                'preferred_season', 'preferred_travel_type', 'age_range', 'budget_range',
                'profile_picture', 'password1', 'password2'
            ),
        }),
    )

    list_display = ('username', 'email', 'first_name', 'last_name', 'mobile_number', 
                    'nationality', 'city', 'preferred_travel_type', 'is_staff', 'is_active')
    
    search_fields = ('username', 'email', 'first_name', 'last_name', 'mobile_number', 'nationality', 'city')
    
    ordering = ('username',)

 
    exclude = ('password',) 
# Register the CustomUser model with the admin site
admin.site.register(CustomUser, CustomUserAdmin)
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'notification_type', 'seen', 'created_at')
    list_filter = ('notification_type', 'seen')
    search_fields = ('user__username', 'message')
    ordering = ('-created_at',)
    actions = ['mark_as_read']

    def mark_as_read(self, request, queryset):
        queryset.update(seen=True)
        self.message_user(request, "Selected notifications marked as read.")
    mark_as_read.short_description = "Mark selected as read"