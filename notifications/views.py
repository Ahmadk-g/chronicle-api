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



class NotificationDetail(generics.RetrieveDestroyAPIView):
    """
    Retrieve a notification and mark it as read.
    """
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Mark the notification as read when accessed."""
        notification = super().get_object()
        if not notification.is_read:
            notification.is_read = True
            notification.save()
        return notification
