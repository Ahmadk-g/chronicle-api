from rest_framework import serializers
from .models import Event


class EventSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
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

    def to_representation(self, instance):
        """
        Override the default `to_representation` method to customize
        how ticket_price is represented.
        """
        representation = super().to_representation(instance)

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
            'location', 'interested_count', 'attending_count'
        ]
