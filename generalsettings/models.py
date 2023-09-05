from django.db import models
from django.db.models import Model, TextField, BooleanField


# Create your models here.


class ApplicationSettings(Model):

    sms_api = TextField(blank=True)
    sms_secret = TextField(blank=True)
    email_jit_api = TextField(blank=True)
    email_jit_secret = TextField(blank=True)
    has_partners = BooleanField()

