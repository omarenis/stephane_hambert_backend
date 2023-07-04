from django.db import models
from django.db.models import Model, DateTimeField
from django.db.models import EmailField
from rest_framework.serializers import ModelSerializer


# Create your models here.
class Subscription(Model):
    email = EmailField(unique=True)
    date_joined = DateTimeField(auto_now_add=True)


class SubscriptionSerializer(ModelSerializer):

    class Meta:
        model = Subscription
        fields = '__all__'
