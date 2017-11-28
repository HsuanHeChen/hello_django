from django.db import models
from django.utils import timezone
from django.conf import settings
from core.models import TimeStampedModel


# Create your models here.


class Union(TimeStampedModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    disabled = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Member(TimeStampedModel):
    union = models.ForeignKey('Union', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.CharField(max_length=128)
    invited_at = models.DateTimeField(auto_now=True)
    join_at = models.DateTimeField(null=True, blank=True)
    quit_at = models.DateTimeField(null=True, blank=True)
