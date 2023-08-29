from django.contrib.auth.models import User
from django.db import models
from django.db.models import Model, URLField, CharField, OneToOneField, CASCADE, BooleanField, BigIntegerField, \
    FloatField, TextField, ForeignKey, SET_NULL, EmailField, DateTimeField
from rest_framework.serializers import ModelSerializer


class CustomerProfile(Model):
    facebook = URLField(blank=True, null=True)
    google = URLField(blank=True, null=True)
    instagram = URLField(blank=True, null=True)
    phone = CharField(max_length=25)
    gender = TextField(null=False, choices=(('male', 'male'), ('female', 'female')))
    has_two_factors_authentication = BooleanField(null=False, default=False)
    user = OneToOneField(to=User, on_delete=CASCADE, null=False)
    number_purchases = BigIntegerField(null=False, default=0)
    total_sales = FloatField(null=False, default=0.0)
    is_banned = BooleanField(null=False, default=False)
    address = TextField(blank=True)
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


class Comment(Model):
    customer = ForeignKey(to='CustomerProfile', null=True, on_delete=SET_NULL)
    product = ForeignKey(to='stock_management.Product', on_delete=CASCADE, null=False)
    content = TextField(null=False)


class CommentSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'


class NotificationForCustomer(Model):

    product = ForeignKey(to='stock_management.Product', on_delete=CASCADE)
    email = EmailField(unique=True)
    date_notification = DateTimeField(auto_now_add=True)
