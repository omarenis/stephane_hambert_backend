from django.contrib.auth.models import AbstractUser
from django.db.models import Model


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
                if hasattr(_object, i) and getattr(_object, i) != data[i]:
                    setattr(_object, i, data[i])
            if data.get('password') is not None and isinstance(_object, AbstractUser) or \
                    issubclass(_object.__class__, AbstractUser):
                _object.set_password(data.get('password'))
            _object.save()
        return _object

    def create(self, data: dict):
        return self.model.objects.create(**data)

    def delete(self, pk):
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
