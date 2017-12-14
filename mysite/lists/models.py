from django.db import models
from django.urls import reverse
from core.models import TimeStampedModel

# Create your models here.


class List(TimeStampedModel):

    def get_absolute_url(self):
        return reverse('lists:view_list', args=[self.id])


class Item(TimeStampedModel):
    text = models.TextField()
    list = models.ForeignKey(List)

    def __str__(self):
        return str(self.pk)
