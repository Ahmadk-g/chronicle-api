from django.db import models
from django.db.models import Count
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_api.permissions import IsOwnerOrReadOnly
from .models import Event
from .serializers import EventSerializer
from rest_framework.response import Response
from rest_framework.views import APIView


class EventList(generics.ListCreateAPIView):
    """
    List events or create a event if logged in
    The perform_create method associates the event with the logged in user.
    """
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Event.objects.annotate(
        interested_count=Count(
            'attendings', filter=models.Q(attendings__status='interested')),
        attending_count=Count(
            'attendings', filter=models.Q(attendings__status='attending'))
    ).order_by('-created_at')

    filter_backends = [
        filters.SearchFilter,
        DjangoFilterBackend,
    ]

    filterset_fields = [
        'owner__followed__owner__profile',
        'attendings__owner__profile',
        'owner__profile',
    ]

    search_fields = [
        'owner__username',
        'title',
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve a post and edit or delete it if you own it.
    """
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
        categories = Event.CATEGORY_CHOICES
        return Response(categories)
