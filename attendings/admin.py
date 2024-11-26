from django.contrib import admin
from .models import Attending

@admin.register(Attending)
class AttendingAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'status', 'event')
    list_filter = ('created_at', 'owner', 'event')
    search_fields = ('owner__username', 'status', 'event__title')
