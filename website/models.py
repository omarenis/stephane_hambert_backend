from django.db import models
from django.db.models import TextField, EmailField


# Create your models here.

class Inscription(models.Model):
    email = EmailField(null=False)

class News(models.Model):

    subject = TextField()
