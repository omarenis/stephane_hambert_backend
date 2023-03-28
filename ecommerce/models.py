from django.db.models import Model, ForeignKey, SET_NULL, CharField, DateTimeField, DecimalField


# Create your models here.
class Order(Model):

    customer = ForeignKey(to='crm.CustomerProfile', on_delete=SET_NULL, null=True)
    paid_at = DateTimeField()
    tva = DecimalField(max_digits=10, decimal_places=2)
    total = DecimalField(max_digits=10, decimal_places=2)
    shipping_method = CharField(max_length=255)
    created_at = DateTimeField(auto_now_add=True)


class OrderLine(Model):

    order = ForeignKey(to='')
