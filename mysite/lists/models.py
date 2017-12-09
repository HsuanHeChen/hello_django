from django.db import models
from core.models import TimeStampedModel

# Create your models here.


class Item(TimeStampedModel):
    text = models.TextField()

    def __str__(self):
        return str(self.pk)
