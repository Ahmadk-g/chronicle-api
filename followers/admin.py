from django.contrib import admin
from .models import Follower


@admin.register(Follower)
class FollowerAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'followed')
    search_fields = ['owner__username', ]
    list_filter = ['owner']
