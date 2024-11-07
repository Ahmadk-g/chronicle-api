from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    """
    Event model, related to 'owner', a User instance.
    Default image set so that we can always reference image.url.
    """

    CATEGORY_CHOICES = [
        ('concert', 'Concert'),
        ('party', 'Party'),
        ('festival', 'Festival'),
        ('exhibition', 'Exhibition'),
        ('workshop', 'Workshop'),
        ('meetup', 'Meetup'),
        ('conference', 'Conference'),
        ('networking', 'Networking'),
        ('seminar', 'Seminar'),
        ('webinar', 'Webinar'),
        ('charity', 'Charity'),
        ('sports', 'Sports'),
        ('food_drink', 'Food & Drink'),
        ('health_wellness', 'Health & Wellness'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(max_length=1000, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ticket_price = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.00
    )
    image = models.ImageField(
        upload_to='images/',
        default='../default_post_b29qkk'
    )
    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES,
        default='meetup'
    )
    event_date = models.DateField(blank=False)
    start_time = models.TimeField(blank=False)
    end_time = models.TimeField(blank=False)
    location = models.CharField(max_length=255, blank=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} by {self.owner.username}'
