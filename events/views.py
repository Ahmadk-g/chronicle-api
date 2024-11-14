from django.db import models
from django.db.models import Count
from rest_framework import generics, permissions
from drf_api.permissions import IsOwnerOrReadOnly
from .models import Event
from .serializers import EventSerializer


class EventList(generics.ListCreateAPIView):

    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Event.objects.annotate(
        interested_count=Count(
            'attendings', filter=models.Q(attendings__status='interested')),
        attending_count=Count(
            'attendings', filter=models.Q(attendings__status='attending'))
    ).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class EventDetail(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = EventSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Event.objects.annotate(
        interested_count=Count(
            'attendings', filter=models.Q(attendings__status='interested')),
        attending_count=Count(
            'attendings', filter=models.Q(attendings__status='attending'))
    ).order_by('-created_at')


class CategoryChoicesView(APIView):
    """
    API endpoint to retrieve the category choices for the Event model.
    """
    def get(self, request):
        # Return the CATEGORY_CHOICES as a JSON response
        categories = Event.CATEGORY_CHOICES
        return Response(categories)