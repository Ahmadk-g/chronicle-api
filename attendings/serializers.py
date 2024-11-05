from django.db import IntegrityError
from rest_framework import serializers
from attendings.models import Attending

class AttendingSerializer(serializers.ModelSerializer):
    """
    Serializer for the Attending model.
    Ensures 'status' is required and handles unique constraint on 'owner' and 'event'.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    status = serializers.ChoiceField(choices=Attending.STATUS_CHOICES, required=True)

    class Meta:
        model = Attending
        fields = ['id', 'created_at', 'owner', 'event', 'status']

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                'detail': 'You have already marked attendance for this event.'
            })
