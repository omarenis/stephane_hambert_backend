from django.db import models
from django.db.models import TextField, EmailField, CharField, Model, ImageField, ForeignKey, CASCADE, FileField


PRODUCT_MODEL = 'stock_management.Product'
# Create your models here.

class Inscription(models.Model):
    email = EmailField(null=False)


class News(models.Model):
    subject = CharField(max_length=255, null=False)
    description = TextField()


class AdditionalInformation(Model):
    type_information = CharField(null=False, choices=(('HISTORY', 'HISTORY'), ('OLFACTIVE', 'OLFACTIVE')))
    image = ImageField(upload_to='histories')
    description = TextField()
    title = CharField(max_length=255)
    product = ForeignKey(to=PRODUCT_MODEL, on_delete=CASCADE)

class AdditionalFile(Model):
    first_image = ImageField()
    second_image = ImageField()
    third_image = ImageField()
    video = FileField()
    product = ForeignKey(to=PRODUCT_MODEL, on_delete=CASCADE)
