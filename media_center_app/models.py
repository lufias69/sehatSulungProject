from django.db import models
from cloudinary.models import CloudinaryField

MEDIA_TYPE_CHOICES = [
    ('image', 'Image'),
    ('video', 'Video'),
]

class MediaItem(models.Model):
    title = models.CharField(max_length=255)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)

    # Gunakan CloudinaryField untuk media
    file = CloudinaryField(resource_type='auto', null=True, blank=True)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
