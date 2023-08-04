from django.db import models
from django.db.models import TextField, EmailField, CharField, Model, ImageField, ForeignKey, CASCADE, FileField, \
    OneToOneField
from rest_framework.serializers import ModelSerializer
from stock_management.models import Product

PRODUCT_MODEL = 'stock_management.Product'


# Create your models here.

class Inscription(models.Model):
    email = EmailField(null=False)


class News(models.Model):
    subject = CharField(max_length=255, null=False)
    description = TextField()


class Olfaction(Model):
    image = ImageField(upload_to='products/olfactions')
    description = TextField()
    title = CharField(max_length=255)
    product = OneToOneField(to=PRODUCT_MODEL, on_delete=CASCADE)


class AdditionalInformationCollection(Model):
    image = ImageField(upload_to='collections/additional_information')
    description = TextField()
    title = CharField(max_length=255)
    collection = ForeignKey(to='stock_management.Collection', on_delete=CASCADE)


class History(models.Model):
    image = ImageField(upload_to='products/histories')
    description = TextField()
    title = CharField(max_length=255)
    product = OneToOneField(to=PRODUCT_MODEL, on_delete=CASCADE)


class AdditionalFile(Model):
    file_or_video = FileField()
    product = ForeignKey(to=PRODUCT_MODEL, on_delete=CASCADE)


class HistorySerializer(ModelSerializer):

    class Meta:
        model = History
        fields = '__all__'


class AdditionalInformationCollectionSerializer(ModelSerializer):

    class Meta:
        model = AdditionalInformationCollection
        fields = '__all__'


class OlfactionSerializer(ModelSerializer):

    class Meta:
        model = Olfaction
        fields = '__all__'


class AdditionalFileSerializer(ModelSerializer):

    class Meta:

        model = AdditionalFile
        fields = '__all__'


class ProductPageModelSerializer(ModelSerializer):
    history = HistorySerializer()
    additional_file_set = AdditionalFileSerializer()
    olfaction = OlfactionSerializer()
    class Meta:

        model = Product
        fields = ['id', 'history', 'olfaction', 'history', 'additional_file_set', 'slug', 'id', 'description', 'price',
                  'image', 'number_purchases']

