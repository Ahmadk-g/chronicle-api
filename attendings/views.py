from rest_framework import generics, permissions
from drf_api.permissions import IsOwnerOrReadOnly
from attendings.models import Attending
from attendings.serializers import AttendingSerializer

class AttendingList(generics.ListCreateAPIView):
    """
    List attendings or create an attendance record.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = AttendingSerializer
    queryset = Attending.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class AttendingDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, edit, or delete an attending record if you own it.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = AttendingSerializer
    queryset = Attending.objects.all()
