from django.db.models import Model, ForeignKey, SET_NULL, CharField, DateTimeField, DecimalField, CASCADE, \
    BigIntegerField, FloatField
from rest_framework.serializers import ModelSerializer


# Create your models here.
class Order(Model):

    customer = ForeignKey(to='crm.CustomerProfile', on_delete=SET_NULL, null=True)
    paid_at = DateTimeField(null=False)
    tva = DecimalField(max_digits=10, decimal_places=2)
    total = DecimalField(max_digits=10, decimal_places=2)
    shipping_method = CharField(max_length=255)
    created_at = DateTimeField(auto_now_add=True)


class OrderLine(Model):

    order = ForeignKey(to='Order', on_delete=CASCADE)
    product = ForeignKey(to='stock_management.Product', on_delete=CASCADE)
    quantity = BigIntegerField(null=False)
    date_order = DateTimeField(auto_now_add=True)
    totalHt = FloatField()


class OrderSerializer(ModelSerializer):

    class Meta:
        db_table = 'orders'
        fields = '__all__'


class OrderLineSerializer(ModelSerializer):

    class Meta:
        db_table = 'order_lines'
        fields = '__all__'
