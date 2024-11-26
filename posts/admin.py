from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'owner', 'updated_at',)
    search_fields = ['title', 'owner__username']
    list_filter = ('created_at', 'updated_at', 'owner', 'image_filter')
