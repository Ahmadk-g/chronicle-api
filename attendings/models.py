from django.db import models
from django.contrib.auth.models import User
from events.models import Event


class Attending(models.Model):

    STATUS_CHOICES = [
        ('interested', 'Interested'),
        ('attending', 'Attending')
    ]
   
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(
        Event, related_name='attendings', on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default=None,
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['owner', 'event']

    def __str__(self):
        return f'{self.owner} {self.event} {self.status}'