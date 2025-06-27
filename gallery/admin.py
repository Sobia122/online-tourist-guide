from django.contrib import admin
from .models import Photo, PhotoInteraction

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ['caption', 'destination', 'uploaded_by', 'tour_type', 'uploaded_at']
    search_fields = ['caption', 'destination__name', 'uploaded_by__username']
    list_filter = ['tour_type', 'uploaded_at']
    fields = ('image', 'caption', 'destination', 'uploaded_by', 'tour_type')
    readonly_fields = ('uploaded_at',)

@admin.register(PhotoInteraction)
class PhotoInteractionAdmin(admin.ModelAdmin):
    list_display = ['user', 'photo', 'liked', 'comment', 'created_at']
    search_fields = ['photo__caption', 'user__username', 'comment']
    list_filter = ['liked', 'created_at']
    readonly_fields = ('created_at',)
