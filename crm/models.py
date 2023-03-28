from django.contrib.auth.models import User
from django.db import models
from django.db.models import Model, URLField, CharField, OneToOneField, CASCADE, BooleanField
from rest_framework.serializers import ModelSerializer


class CustomerProfile(Model):

    AUTH_FACTOR_METHODS = (('email', 'email'), ('phone', 'phone'))

    facebook = URLField()
    google = URLField()
    phone = CharField(max_length=25)
    user = OneToOneField(to=User, on_delete=CASCADE, null=False)

    class Meta:
        db_table = 'customers'


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CustomerSerialize(ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = CustomerProfile
        fields = '__all__'
