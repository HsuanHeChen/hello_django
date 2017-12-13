from django.db import models
from core.models import TimeStampedModel

# Create your models here.


class List(TimeStampedModel):
    pass

class Item(TimeStampedModel):
    text = models.TextField()
    list = models.ForeignKey(List)

    def __str__(self):
        return str(self.pk)
