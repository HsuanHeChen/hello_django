from django.db import models
from django.utils import timezone
from core.models import TimeStampedModel
from .managers import PublishedManager, VoucherManager

# Create your models here.


class Product(TimeStampedModel):
    name = models.CharField(max_length=200)
    sku = models.CharField(blank=True, max_length=100)
    photo = models.URLField(blank=True)
    enabled = models.BooleanField(default=False)
    press = models.IntegerField(default=0)  # 點擊次數

    def __str__(self):
        return self.name


class Review(TimeStampedModel):
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    photo = models.URLField(blank=True)
    location = models.CharField(blank=True, max_length=100)
    published_at = models.DateTimeField(auto_now=True)
    objects = PublishedManager()

    def __str__(self):
        return self.title


class Voucher(TimeStampedModel):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    address = models.TextField()
    birth_date = models.DateField(blank=True)
    sent = models.BooleanField(default=False)
    redeemed = models.BooleanField(default=False)
    objects = VoucherManager()
