from django.db.models import Model, CharField, FloatField, BigIntegerField, TextField, DateTimeField, ForeignKey, \
    CASCADE, SET_NULL, ImageField, SlugField, ManyToManyField
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
    collection = ForeignKey(to='Collection', on_delete=SET_NULL, null=True, blank=True)
    category_set = ManyToManyField(to='Category', null=True, blank=True)
    promo = ForeignKey(to='Promo', on_delete=SET_NULL, null=True)
    updated_at = DateTimeField(auto_now_add=True)
    slug = SlugField(null=False)

    def __str__(self):
        return self.slug

    class Meta:
        db_table = 'products'


class Category(Model):
    title = CharField(max_length=255, unique=True)
    number_products = BigIntegerField(null=False, default=0)
    number_purchases = BigIntegerField(null=False, default=0)
    total_gain = FloatField(null=False, default=0.0)
    def __str__(self):
        return self.title

    class Meta:
        db_table = 'categories'


class Collection(Model):
    image = ImageField(upload_to='mages/collections', null=False)
    title = CharField(null=False, unique=True, max_length=255)
    content = TextField(null=False)
    number_products = BigIntegerField(null=False, default=0)
    number_purchases = BigIntegerField(null=False, default=0)
    total_gain = FloatField(null=False, default=0.0)
    citation = TextField(blank=True)

    def __str__(self):
        return self.title

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

    def __str__(self):
        return self.label

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


class ProductListSerializer(ModelSerializer):
    class Meta:
        model = Product


class ProductSerializer(ModelSerializer):
    collection = CollectionSerializer(read_only=True)
    promo = PromoSerializer(read_only=True)
    category_set = CategorySerializer(read_only=True)
    comment_set = CommentSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'code', 'description', 'price', 'current_quantity', 'tva', 'image', 'number_purchases',
                  'ingredients', 'collection', 'citation', 'promo', 'category', 'comment_set', 'history']
