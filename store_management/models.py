from django.db.models import Model, TextField, ForeignKey, SET_NULL, IntegerField, ImageField


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
    number_products  = IntegerField(null=False, default=0)
    promo = ForeignKey(to='stock_management.Promo', on_delete=SET_NULL, null=True)
