from django.db import models
from django.db.models import Model, TextField, ForeignKey, CASCADE
from django.contrib.auth.models import User


# Create your models here.
class Message(Model):
    message = TextField()
    sender = ForeignKey(to=User, on_delete=CASCADE)
    receiver = ForeignKey(to=User, on_delete=CASCADE)


