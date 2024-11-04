from rest_framework import generics, permissions
from .models import Notification
from .serializers import NotificationSerializer

class NotificationList(generics.ListAPIView):
    queryset = Notification.objects.all()

    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]  # Ensure user is authenticated

    def get_queryset(self):
        """Return notifications for the authenticated user."""
        return self.queryset.filter(owner=self.request.user)

    def perform_update(self, serializer):
        """Override the default update method to mark notifications as read."""
        notification = serializer.save()
        if 'is_read' in self.request.data and self.request.data['is_read']:
            notification.mark_as_read()
