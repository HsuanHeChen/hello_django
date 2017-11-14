from django.db import models
from core.models import TimeStampedModel

# Create your models here.

class Review(TimeStampedModel):
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    photo = models.URLField(blank=True)
    location = models.CharField(blank=True, max_length=100)

    def __str__(self):
        return self.title