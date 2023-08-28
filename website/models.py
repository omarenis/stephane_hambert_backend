from django.db import models
from django.db.models import TextField, EmailField, CharField, Model, ImageField, ForeignKey, CASCADE, FileField, \
    OneToOneField
from rest_framework.serializers import ModelSerializer
from stock_management.models import Product, Collection, CategorySerializer, PromoSerializer

PRODUCT_MODEL = 'stock_management.Product'


# Create your models here.

class Inscription(models.Model):
    email = EmailField(null=False)


class Notification(Model):

    product = ForeignKey(to='stock_management.Product', on_delete=CASCADE, null=False)
    customer = ForeignKey(to='crm.CustomerProfile', on_delete=CASCADE, null=False)
class News(models.Model):
    subject = CharField(max_length=255, null=False)
    description = TextField()


class Olfaction(Model):
    image = ImageField(upload_to='products/olfactions')
    content  = TextField()
    title = CharField(max_length=255)
    product = OneToOneField(to=PRODUCT_MODEL, on_delete=CASCADE)


class AdditionalInformationCollection(Model):
    image = ImageField(upload_to='collections/additional_information')
    content = TextField()
    title = CharField(max_length=255)
    collection = ForeignKey(to='stock_management.Collection', on_delete=CASCADE)


class History(models.Model):
    image = ImageField(upload_to='products/histories')
    content = TextField()
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


class CollectionSerializer(ModelSerializer):
    additionalinformationcollection_set = AdditionalInformationCollectionSerializer()

    class Meta:
        model = Collection
        fields = ['id', 'image', 'title', 'citation', 'content', 'additionalinformationcollection_set']

class ProductListSerializer(ModelSerializer):
    promo = PromoSerializer(read_only=True)
    class Meta:
        model  = Product
        fields = ['slug', 'title', 'price', 'image', 'promo']

class ProductPageModelSerializer(ModelSerializer):
    history = HistorySerializer()
    additionalfile_set = AdditionalFileSerializer(read_only=True, many=True, allow_null=True)
    olfaction = OlfactionSerializer()

    class Meta:
        model = Product
        fields = ['id', 'history', 'olfaction', 'history', 'additionalfile_set', 'slug', 'id', 'description', 'price',
                  'image']
