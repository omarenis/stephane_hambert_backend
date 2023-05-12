from django.db import models
from django.db.models import Model, TextField, ForeignKey, SET_NULL


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
