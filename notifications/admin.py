from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'owner', 'notifier', 'notification_type',
        'post', 'event', 'is_read', 'created_at'
    )
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = (
        'owner__username', 'notifier__username',
        'notification_type', 'post__title', 'event__title'
    )
    ordering = ['-created_at']
