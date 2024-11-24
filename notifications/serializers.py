from datetime import timedelta
from django.utils.timezone import now
from django.contrib.humanize.templatetags.humanize import naturaltime
from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    notifier_name = serializers.ReadOnlyField(source='notifier.username')
    notifier_image = serializers.ReadOnlyField(source='notifier.profile.image.url')
    notifier_id = serializers.ReadOnlyField(source='notifier.profile.id')
    post_image = serializers.ReadOnlyField(source='post.image.url')
    event_image = serializers.ReadOnlyField(source='event.image.url')
    created_at = serializers.SerializerMethodField()

    # def get_created_at(self, obj):
    #     return naturaltime(obj.created_at)

    def get_created_at(self, obj):
        time_diff = now() - obj.created_at
        if time_diff >= timedelta(weeks=1):
            # Return a rounded weeks output for over 1 week
            weeks = time_diff.days // 7
            return f"{weeks} week{'s' if weeks > 1 else ''} ago"
        elif time_diff >= timedelta(days=1):
            # Return a rounded days output for over 1 day
            return f"{time_diff.days} day{'s' if time_diff.days > 1 else ''} ago"
        else:
            # For less than 1 day, fallback to the standard naturaltime
            return naturaltime(obj.created_at)

    class Meta:
        model = Notification
        fields = [
            'id', 'owner', 'notifier_name', 'notifier_image',
            'notifier_id','notification_type','post', 'event',
            'post_image', 'event_image', 'is_read', 'created_at'
        ]

    def mark_as_read(self, instance):
        instance.is_read = True
        instance.save()
