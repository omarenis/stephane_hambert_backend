from django.db import models
from django.db.models import TextField, EmailField, CharField, Model, ImageField, ForeignKey, CASCADE, FileField, \
    OneToOneField
from rest_framework.serializers import ModelSerializer
from stock_management.models import Product, Collection, CategorySerializer, PromoSerializer

PRODUCT_MODEL = 'stock_management.Product'


# Create your models here.


class Notification(Model):
    product = ForeignKey(to='stock_management.Product', on_delete=CASCADE, null=False)
    email  = EmailField(null=False)


class Olfaction(Model):
    image = ImageField(upload_to='images/products/olfactions')
    content = TextField()
    title = CharField(max_length=255)
    product = OneToOneField(to=PRODUCT_MODEL, on_delete=CASCADE)


class Present(Model):
    image = ImageField(upload_to='images/presents')
    content = TextField(blank=True)
    title = CharField(max_length=255, unique=True)

    class Meta:

        db_table = 'presents'

class AdditionalInformationCollection(Model):
    image = ImageField(upload_to='images/collections/additional_information')
    content = TextField()
    title = CharField(max_length=255)
    collection = ForeignKey(to='stock_management.Collection', on_delete=CASCADE)


class History(models.Model):
    image = ImageField(upload_to='images/products/histories')
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


class PresentSerializer(ModelSerializer):

    class Meta:
        model = Present
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
    additionalinformationcollection_set = AdditionalInformationCollectionSerializer(many=True, read_only=True)

    class Meta:
        model = Collection
        fields = ['id', 'image', 'title', 'citation', 'content', 'additionalinformationcollection_set']


class ProductListSerializer(ModelSerializer):
    promo = PromoSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['slug', 'title', 'price', 'image', 'promo']


class ProductPageModelSerializer(ModelSerializer):
    history = HistorySerializer()
    additionalfile_set = AdditionalFileSerializer(read_only=True, many=True, allow_null=True)
    olfaction = OlfactionSerializer()

    class Meta:
        model = Product
        fields = ['id', 'title', 'history', 'olfaction', 'history', 'additionalfile_set', 'slug', 'id', 'description', 'price',
                  'image']
