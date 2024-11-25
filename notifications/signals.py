from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Notification
from followers.models import Follower
from likes.models import Like
from comments.models import Comment
from posts.models import Post
from attendings.models import Attending
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Follower)
def create_follower_notification(sender, instance, created, **kwargs):
    try:
        if created:
            Notification.objects.create(
                owner=instance.followed,
                notifier=instance.owner,
                notification_type='follow',
            )
    except Exception as e:
        logger.error(f"Failed to create follow notification: {e}")


@receiver(post_delete, sender=Follower)
def delete_follow_notification(sender, instance, **kwargs):
    # Delete the "follow" notification when a follow is removed
    try:
        Notification.objects.filter(
            owner=instance.followed,
            notifier=instance.owner,
            notification_type='follow',
        ).delete()
    except Exception as e:
        logger.error(f"Failed to delete follow notification: {e}")


@receiver(post_save, sender=Like)
def create_like_notification(sender, instance, created, **kwargs):
    try:
        if created:
            Notification.objects.create(
                owner=instance.post.owner,
                notifier=instance.owner,
                notification_type='like',
                post=instance.post,
            )
    except Exception as e:
        logger.error(f"Failed to create like notification: {e}")


@receiver(post_delete, sender=Like)
def delete_like_notification(sender, instance, **kwargs):
    # Delete the "like" notification when a like is removed
    try:
        Notification.objects.filter(
            owner=instance.post.owner,
            notifier=instance.owner,
            notification_type='like',
            post=instance.post
        ).delete()
    except Exception as e:
        logger.error(f"Failed to delete like notification: {e}")


@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    try: 
        if created:
            # Check if the comment owner is not the same as the post owner
            if instance.owner != instance.post.owner:
                Notification.objects.create(
                    owner=instance.post.owner,
                    notifier=instance.owner,
                    notification_type='comment',
                    post=instance.post,
                )
    except Exception as e:
        logger.error(f"Failed to create comment notification: {e}")


@receiver(post_delete, sender=Comment)
def delete_comment_notification(sender, instance, **kwargs):
    try:
        Notification.objects.filter(
            owner=instance.post.owner,
            notifier=instance.owner,
            notification_type='comment',
            post=instance.post
        ).delete()
    except Exception as e:
        logger.error(f"Failed to delete comment notification: {e}")

@receiver(post_save, sender=Attending)
def create_update_attendance_notification(sender, instance, created, **kwargs):
    try:
        if created:
            # Only create a notification if it's a new record
            Notification.objects.create(
                owner=instance.event.owner,
                notifier=instance.owner,
                notification_type=instance.status,
                event=instance.event,
            )
        elif getattr(instance, '_status_changed', False):
            # Handle status updates (delete old notification and create a new one)
            Notification.objects.filter(
                owner=instance.event.owner,
                notifier=instance.owner,
                event=instance.event
            ).delete()

            Notification.objects.create(
                owner=instance.event.owner,
                notifier=instance.owner,
                notification_type=instance.status,
                event=instance.event,
            )
    except Exception as e:
        logger.error(f"Failed to create or update attendance notification: {e}")

@receiver(post_delete, sender=Attending)
def delete_attendance_notification(sender, instance, **kwargs):
    try:
        Notification.objects.filter(
            owner=instance.event.owner,
            notifier=instance.owner,
            event=instance.event
        ).delete()
    except Exception as e:
        logger.error(f"Failed to delete attendance notification: {e}")
