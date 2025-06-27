from django.contrib import admin
from django.utils.html import format_html
from .models import TravelTip

@admin.register(TravelTip)
class TravelTipAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'season', 'tip_type', 'approved', 'created_at', 'share_on_facebook', 'share_on_twitter')
    list_filter = ('approved', 'season', 'tip_type')
    search_fields = ('title', 'user__username')
    actions = ['approve_tips', 'reject_tips']

    def approve_tips(self, request, queryset):
        queryset.update(approved=True)
        self.message_user(request, "Selected tips have been approved.")
    approve_tips.short_description = "✅ Approve selected tips"

    def reject_tips(self, request, queryset):
        queryset.update(approved=False)
        self.message_user(request, "Selected tips have been rejected.")
    reject_tips.short_description = "❌ Reject selected tips"

    def save_model(self, request, obj, form, change):
        # If admin is editing the tip
        if request.user.is_superuser and change:
            changed_fields = form.changed_data
            editable_fields = ['title', 'content', 'season', 'tip_type']
            if any(field in changed_fields for field in editable_fields):
                obj.user = request.user  # Admin modified content → make admin the user
        elif not change:
            obj.user = request.user  # New tip by admin

        super().save_model(request, obj, form, change)

    def share_on_facebook(self, obj):
        url = f"https://www.facebook.com/sharer/sharer.php?u=https://yourdomain.com/tips/{obj.id}/"
        return format_html('<a class="button" href="{}" target="_blank">Facebook</a>', url)
    share_on_facebook.short_description = "📘 Share"

    def share_on_twitter(self, obj):
        url = f"https://twitter.com/intent/tweet?text={obj.title}&url=https://yourdomain.com/tips/{obj.id}/"
        return format_html('<a class="button" href="{}" target="_blank">Twitter</a>', url)
    share_on_twitter.short_description = "🐦 Tweet"
