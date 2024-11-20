from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Notification
from followers.models import Follower
from likes.models import Like
from comments.models import Comment
from posts.models import Post
from attendings.models import Attending


@receiver(post_save, sender=Follower)
def create_follower_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            owner=instance.followed,
            notifier=instance.owner,
            notification_type='follow',
        )


@receiver(post_save, sender=Like)
def create_like_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            owner=instance.post.owner,
            notifier=instance.owner,
            notification_type='like',
            post=instance.post,
        )


@receiver(post_delete, sender=Like)
def delete_like_notification(sender, instance, **kwargs):
    # Delete the "like" notification when a like is removed
    Notification.objects.filter(
        owner=instance.post.owner,
        notifier=instance.owner,
        notification_type='like',
        post=instance.post
    ).delete()


@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    if created:
        # Check if the comment owner is not the same as the post owner
        if instance.owner != instance.post.owner:
            Notification.objects.create(
                owner=instance.post.owner,
                notifier=instance.owner,
                notification_type='comment',
                post=instance.post,
            )


@receiver(post_save, sender=Attending)
def create_update_attendance_notification(sender, instance, created, **kwargs):
    if created or getattr(instance, '_status_changed', False):
        # Delete existing notifications for the event by the same notifier
        Notification.objects.filter(
            owner=instance.event.owner,
            notifier=instance.owner,
            event=instance.event
        ).delete()

        # Create a new notification based on the new status
        Notification.objects.create(
            owner=instance.event.owner,
            notifier=instance.owner,
            notification_type=instance.status,
            event=instance.event,
        )
