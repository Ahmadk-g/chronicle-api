from django.db import models
from django.contrib.auth.models import User
from posts.models import Post
from events.models import Event


class Notification(models.Model):
    """
    Notification model, related to 'owner' and 'notifier'.
    'owner' is the user receiving the notification, and 'notifier' is the user who triggered it.
    Tracks different types of notifications related to actions.
    """

    NOTIFICATION_TYPES = [
        ('follow', 'Follow'),
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('interested', 'Interested'),
        ('attending', 'Attending')
    ]
    
    owner = models.ForeignKey(
        User,
        related_name='notifications',
        on_delete=models.CASCADE
    )  # User receiving the notification
    notifier = models.ForeignKey(
        User, related_name='notifications_sent', on_delete=models.CASCADE)  # User who triggered the notification
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)  # Reference to the related post, if applicable
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True)  # Reference to the related event, if applicable
    is_read = models.BooleanField(default=False)  # Notification read status
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        post_info = f" on post'{self.post.title}'" if self.post else ""  # Get the title if it exists
        event_info = f" on event'{self.event.title}'" if self.event else ""  # Get the title if it exists
        return f"{self.notifier.username} {self.notification_type} {self.owner.username} - {post_info} - {event_info}"
