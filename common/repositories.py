import os

from django.contrib.auth.models import AbstractUser
from django.db.models import Model, FileField, ImageField
from django.db.models.fields.files import FieldFile


class Repository(object):
    def __init__(self, model: Model or AbstractUser, database='default'):
        self.model = model
        self.database = database

    def list(self):
        return self.model.objects.all()

    def retrieve_by_id(self, pk: int):
        return self.model.objects.get(id=pk)

    def retrieve(self, data):
        try:
            return self.model.objects.get(**data)
        except self.model.DoesNotExist:
            raise self.model.DoesNotExist('item does not exists with the specified data')

    def put(self, pk: int, data: dict):
        _object = self.model.objects.get(id=pk)
        if _object is None:
            return Exception('object not found')
        else:
            for i in data:
                if hasattr(_object, i):
                    if isinstance(getattr(_object, i), FieldFile) or issubclass(getattr(_object, i).__class__, FieldFile):
                        self.delete_file_from_object(file_field=getattr(_object, i))
                    setattr(_object, i, data[i])
            if data.get('password') is not None and isinstance(_object, AbstractUser) or \
                    issubclass(_object.__class__, AbstractUser):
                _object.set_password(data.get('password'))
            _object.save()
        return _object

    @staticmethod
    def delete_file_from_object(file_field: FieldFile):
        path = file_field.path
        if os.path.exists(path):
            os.remove(path=path)

    def create(self, data: dict):
        return self.model.objects.create(**data)

    def delete(self, pk):
        instance = self.model.objects.get(pk=pk)
        if instance is not None:
            for field in getattr(instance, '_meta').get_fields(include_parents=False):
                if isinstance(field, FileField):
                    self.delete_file_from_object(instance=instance, file_field=field)
        return self.model.objects.get(pk=pk).delete()

    def filter_by(self, data: dict, start=0, end=None, order_by=None):
        data = self.model.objects.filter(**data)
        if order_by is not None and isinstance(order_by, list) and order_by != []:
            for args in order_by:
                data = data.order_by(args)
        if end is not None:
            data = data[start:]
        else:
            data = data[start: end]
        return data
