from django.db import models
from django.db.models import TextField, EmailField, CharField, Model, ImageField, ForeignKey


# Create your models here.

class Inscription(models.Model):
    email = EmailField(null=False)


class News(models.Model):
    subject = CharField(max_length=255, null=False)
    description = TextField()


class HistoryProduct(Model):
    image = ImageField(upload_to='histories')
    description = TextField()
    title = CharField(max_length=255)
    product = ForeignKey(to='stock_management.Product')


class Olfactory(models.Model):
    image = ImageField(upload_to='histories')
    description = TextField()
    title = CharField(max_length=255)
