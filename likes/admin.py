from django.contrib import admin
from .models import Like


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'post', 'created_at')
    list_filter = ('owner', 'post')
    search_fields = ('owner__username', 'post__title')
