from django.db.models import Model, TextField, ForeignKey, SET_NULL, IntegerField, ImageField
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.serializers import FileField

# Create your models here.
class Localisation(Model):
    country = TextField()
    city = TextField()
    zip_code = TextField()
    altitude = TextField()
    longitude = TextField()


class Store(Model):
    label = TextField()
    localisation = ForeignKey(to='Localisation', on_delete=SET_NULL, null=True)
    image = ImageField(upload_to='stores')
    number_products = IntegerField(null=False, default=0)
    promo = ForeignKey(to='stock_management.Promo', on_delete=SET_NULL, null=True)


class LocalisationSerializer(ModelSerializer):

    class Meta:
        model = Localisation
        fields = '__all__'


class StoreSerializer(ModelSerializer):
    localisation = LocalisationSerializer(read_only=True)
    image = FileField()
    class Meta:

        model = Store
        label = TextField()
        fields = ['id', 'label', 'image', 'number_products', 'promo']
