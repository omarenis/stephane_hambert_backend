from django.db import models
from django.db.models import Model


# Create your models here.

class Image(Model):
    src = models.URLField(max_length=255)
    alt = models.CharField(max_length=255)


class TextBlock(Model):
    content = models.TextField(max_length=255)


class Card(Model):
    style = models.CharField(max_length=255)
    image = models.ImageField(max_length=255, null=True)
    title = models.CharField(max_length=255, blank=True)
    block = models.CharField(max_length=255, blank=True)
