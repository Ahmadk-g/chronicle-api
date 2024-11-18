from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    notifier_name = serializers.ReadOnlyField(source='notifier.username')
    notifier_image = serializers.ReadOnlyField(source='notifier.profile.image.url')
    notifier_id = serializers.ReadOnlyField(source='notifier.profile.id')

    class Meta:
        model = Notification
        fields = [
            'id', 'owner', 'notifier_name', 'notifier_image',
            'notifier_id','notification_type','post', 'event',
            'is_read', 'created_at'
        ]

    def mark_as_read(self, instance):
        instance.is_read = True
        instance.save()
