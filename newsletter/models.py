from django.db import models
from django.db.models import Model
from django.db.models import EmailField


# Create your models here.
class Inscription(Model):
    email = EmailField()
