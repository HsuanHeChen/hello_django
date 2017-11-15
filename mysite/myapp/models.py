from django.db import models
from django.utils import timezone
from core.models import TimeStampedModel

# Create your models here.


class PublishedManager(models.Manager):
    use_for_related_fields = True

    def published(self, **kwargs):
        return self.filter(published_at__lte=timezone.now(), **kwargs)


class Product(TimeStampedModel):
    name = models.CharField(max_length=200)
    sku =  models.CharField(blank=True, max_length=100)
    photo = models.URLField(blank=True)
    
    def __str__(self):
        return self.name


class Review(TimeStampedModel):
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    photo = models.URLField(blank=True)
    location = models.CharField(blank=True, max_length=100)
    published_at = models.DateTimeField(null=True, blank=True)

    objects = PublishedManager()

    def __str__(self):
        return self.title
