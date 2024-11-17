from rest_framework import serializers
from .models import Event
from attendings.models import Attending


class EventSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    attendance_id = serializers.SerializerMethodField()
    interested_count = serializers.ReadOnlyField()
    attending_count = serializers.ReadOnlyField()

    def validate_ticket_price(self, value):
        if value is not None:
            if value < 0:
                raise serializers.ValidationError(
                    'Ticket price cannot be negative!')
        return value

    def validate_image(self, value):
        if value.size > 2 * 1024 * 1024:
            raise serializers.ValidationError('Image size larger than 2MB!')
        if value.image.height > 4096:
            raise serializers.ValidationError(
                'Image height larger than 4096px!'
            )
        if value.image.width > 4096:
            raise serializers.ValidationError(
                'Image width larger than 4096px!'
            )
        return value

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_attendance_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            attending = Attending.objects.filter(
                owner=user, event=obj
            ).first()
            return attending.id if attending else None
        return None

    def to_representation(self, instance):
        """
        Override the default `to_representation` method to:
        Format how ticket_price is represented.
        Format start_time, end_time, and event_date.
        """
        representation = super().to_representation(instance)

        # Format start_time and end_time to 'HH:MM'
        representation['start_time'] = instance.start_time.strftime("%H:%M") if instance.start_time else None
        representation['end_time'] = instance.end_time.strftime("%H:%M") if instance.end_time else None

        # Format event_date to 'DD MMM YYYY'
        representation['event_date'] = instance.event_date.strftime("%d %b %Y") if instance.event_date else None

        # Modify the ticket_price field
        if instance.ticket_price == 0.00:
            representation['ticket_price'] = "Free"
        else:
            representation['ticket_price'] = f"€{instance.ticket_price:.2f}"

        return representation

    class Meta:
        model = Event
        fields = [
            'id', 'owner', 'is_owner', 'profile_id',
            'profile_image', 'created_at', 'updated_at',
            'title', 'description', 'image', 'ticket_price',
            'event_date', 'start_time', 'end_time', 'category',
            'location', 'attendance_id','interested_count', 'attending_count'
        ]
