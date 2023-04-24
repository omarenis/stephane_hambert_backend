from django.contrib.auth.models import User
from django.db import models
from django.db.models import Model, URLField, CharField, OneToOneField, CASCADE, BooleanField, BigIntegerField, \
    FloatField, TextField
from rest_framework.serializers import ModelSerializer


class CustomerProfile(Model):
    facebook = URLField(null=True)
    google = URLField(null=True)
    phone = CharField(max_length=25)
    gender = TextField(null=False, choices=(('male', 'male'), ('female', 'female')))
    has_two_factors_authentication = BooleanField(null=False, default=False)
    user = OneToOneField(to=User, on_delete=CASCADE, null=False)
    number_purchases = BigIntegerField(null=False, default=0)
    total_sales = FloatField(null=False, default=0.0)

    class Meta:
        db_table = 'customers'


class CustomerProfileSerializer(ModelSerializer):
    class Meta:
        model = CustomerProfile
        exclude = ['user']


class UserSerializer(ModelSerializer):
    customerprofile = CustomerProfileSerializer(read_only=True)

    class Meta:
        model = User
        exclude = ('password',)

