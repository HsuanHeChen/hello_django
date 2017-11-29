from django.db import models
from django.urls import reverse
from django.conf import settings
from core.models import TimeStampedModel


# Create your models here.


class Union(TimeStampedModel):
    name = models.CharField(max_length=200)
    disabled = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('unionapp:detial', kwargs={'pk': self.pk})


class Member(TimeStampedModel):
    union = models.ForeignKey('Union', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.CharField(blank=True, max_length=128)
    invited_at = models.DateTimeField(auto_now=True)
    join_at = models.DateTimeField(null=True, blank=True)
    quit_at = models.DateTimeField(null=True, blank=True)
    is_admin = models.BooleanField(default=False)
