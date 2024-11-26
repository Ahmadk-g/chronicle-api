from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer


class NotificationList(generics.ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

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


class MarkAllNotificationsAsRead(generics.GenericAPIView):
    """
    Mark all notifications for the logged-in user as read.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NotificationSerializer

    def patch(self, request, *args, **kwargs):
        notifications = Notification.objects.filter(owner=request.user, is_read=False)
        
        # Update the notifications to mark them as read
        updated_count = notifications.update(is_read=True)

        # Return response with the count of updated notifications
        return Response({"message": f"All notifications marked as read. ({updated_count} notifications updated)"})