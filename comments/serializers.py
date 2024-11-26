from datetime import timedelta
from django.utils.timezone import now
from django.contrib.humanize.templatetags.humanize import naturaltime
from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Comment model.
    Transforms Comment model instances into JSON format, including additional fields
    like the owner's username, profile details, and human-readable timestamps.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_created_at(self, obj):
        time_diff = now() - obj.created_at
        if time_diff >= timedelta(weeks=1):
            weeks = time_diff.days // 7
            return f"{weeks} week{'s' if weeks > 1 else ''} ago"
        elif time_diff >= timedelta(days=1):
            return f"{time_diff.days} day{'s' if time_diff.days > 1 else ''} ago"
        else:
            return naturaltime(obj.created_at)
    
    def get_updated_at(self, obj):
        time_diff = now() - obj.updated_at
        if time_diff >= timedelta(weeks=1):
            weeks = time_diff.days // 7
            return f"{weeks} week{'s' if weeks > 1 else ''} ago"
        elif time_diff >= timedelta(days=1):
            return f"{time_diff.days} day{'s' if time_diff.days > 1 else ''} ago"
        else:
            return naturaltime(obj.updated_at)

    class Meta:
        model = Comment
        fields = [
            'id', 'owner', 'is_owner', 'profile_id',
            'profile_image', 'post', 'created_at',
            'updated_at', 'content'
        ]


class CommentDetailSerializer(CommentSerializer):
    """
    Serializer for detailed Comment information, inheriting from CommentSerializer.
    Adds the post ID to the serialized data.
    """
    post = serializers.ReadOnlyField(source='post.id')
