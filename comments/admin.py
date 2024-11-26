from django.contrib import admin
from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'post', 'updated_at', 'content')
    list_filter = ('created_at', 'updated_at', 'owner')
    search_fields = ('owner__username', 'content', 'post__title')
