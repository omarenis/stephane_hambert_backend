from django.db.models import Model, CharField, FloatField, BigIntegerField, TextField, DateTimeField, ForeignKey, \
    CASCADE, SET_NULL, ImageField
from rest_framework.serializers import ModelSerializer, ImageField as ImageFieldSerializer
from crm.models import CommentSerializer


# Create your models here.
class Product(Model):
    title = CharField(null=False, unique=True, max_length=255)
    code = CharField(null=False, unique=True, max_length=255)
    description = TextField(null=False)
    price = FloatField(null=False)
    current_quantity = BigIntegerField(null=False, default=1)
    tva = FloatField(null=False)
    image = ImageField(upload_to='images/products', null=False)
    number_purchases = BigIntegerField(null=False, default=0)
    ingredients = TextField(null=False)
    collection = ForeignKey(to='Collection', on_delete=SET_NULL, null=True)
    category = ForeignKey(to='Category', on_delete=SET_NULL, null=True)
    promo = ForeignKey(to='Promo', on_delete=SET_NULL, null=True)
    updated_at = DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'products'


class Category(Model):
    title = CharField(max_length=255, unique=True)
    number_products = BigIntegerField(null=False, default=0)
    number_purchases = BigIntegerField(null=False, default=0)
    total_gain = FloatField(null=False, default=0.0)

    class Meta:
        db_table = 'categories'


class Collection(Model):
    image = ImageField(upload_to='mages/collections', null=False)
    label = CharField(null=False, unique=True, max_length=255)
    description = TextField(null=False)
    number_products = BigIntegerField(null=False, default=0)
    number_purchases = BigIntegerField(null=False, default=0)
    total_gain = FloatField(null=False, default=0.0)

    class Meta:
        db_table = 'collections'


class Promo(Model):
    label = CharField(null=False, unique=True, max_length=255)
    datetime_start = DateTimeField(null=False)
    datetime_end = DateTimeField(null=False)
    percentage = FloatField(null=False)
    number_products = BigIntegerField(null=False, default=0)
    number_purchases = BigIntegerField(null=False, default=0)
    total_gain = FloatField(null=False, default=0.0)

    class Meta:
        db_table = 'promos'


class CollectionSerializer(ModelSerializer):
    class Meta:
        model = Collection
        fields = '__all__'


class PromoSerializer(ModelSerializer):
    class Meta:
        model = Promo
        fields = '__all__'


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(ModelSerializer):
    collection = CollectionSerializer(read_only=True)
    promo = PromoSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    comment_set = CommentSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'code', 'description', 'price', 'current_quantity', 'tva', 'image', 'number_purchases',
                  'ingredients', 'collection', 'promo', 'category', 'comment_set']
