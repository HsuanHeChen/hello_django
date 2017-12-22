from django.conf import settings
from django.db import models
from django.urls import reverse
from core.models import TimeStampedModel

# Create your models here.


class List(TimeStampedModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('lists:view_list', args=[self.id])

    @staticmethod
    def create_new(first_item_text, owner=None):
        _list = List.objects.create(owner=owner)
        Item.objects.create(text=first_item_text, list=_list)
        return _list

    @property
    def name(self):
        return self.item_set.first().text


class Item(TimeStampedModel):
    text = models.TextField(default='')
    list = models.ForeignKey(List)

    class Meta:
        unique_together = ('list', 'text')

    def __str__(self):
        return str(self.pk)
