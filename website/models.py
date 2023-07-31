from django.db import models
from django.db.models import TextField, EmailField, CharField, Model, ImageField, ForeignKey, CASCADE, FileField, \
    OneToOneField

PRODUCT_MODEL = 'stock_management.Product'
# Create your models here.

class Inscription(models.Model):
    email = EmailField(null=False)


class News(models.Model):
    subject = CharField(max_length=255, null=False)
    description = TextField()


class History(Model):
    image = ImageField(upload_to='histories')
    description = TextField()
    title = CharField(max_length=255)
    product = OneToOneField(to=PRODUCT_MODEL, on_delete=CASCADE)


class OlfactiveProduct(Model):
    image = ImageField(upload_to='histories')
    description = TextField()
    title = CharField(max_length=255)
    product = OneToOneField(to=PRODUCT_MODEL, on_delete=CASCADE)


class AdditionalFilesProduct(Model):
    first_image = ImageField()
    second_image = ImageField()
    third_image = ImageField()
    video = FileField()
    product = OneToOneField(to=PRODUCT_MODEL, on_delete=CASCADE)


class OtherInformationCollection(Model):
    image = ImageField(upload_to='histories')
    content = TextField()
    title = CharField(max_length=255)
    product = OneToOneField(to='stock_management.Collection', on_delete=CASCADE)
