from django.contrib import admin
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'owner', 'category', 'event_date', 'start_time',
        'ticket_price', 'location', 'created_at'
    )
    list_filter = ('category', 'event_date', 'owner')
    search_fields = ('title', 'owner__username', 'description', 'location')
    ordering = ['-created_at']
