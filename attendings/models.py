from django.db import models
from django.contrib.auth.models import User
from events.models import Event


class Attending(models.Model):
    """
    Attending model, related to 'owner' and 'event'.
    'owner' is a User instance and 'event' is an Event instance.
    Tracks the attendance status of the user for the event.
    """

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
        blank=False,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['owner', 'event']

    def __str__(self):
        return f'{self.owner} {self.event} {self.status}'

    def save(self, *args, **kwargs):
        # Check if the instance is being updated and the status has changed
        if self.pk is not None:
            previous = Attending.objects.get(pk=self.pk)
            if previous.status != self.status:
                self._status_changed = True  # Set flag to track status change
        else:
            self._status_changed = False  # New instance, no change yet

        super().save(*args, **kwargs)
