from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification
from followers.models import Follower
from likes.models import Like
from comments.models import Comment
from posts.models import Post

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

@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            owner=instance.post.owner,
            notifier=instance.owner,
            notification_type='comment',
            post=instance.post,
        )
