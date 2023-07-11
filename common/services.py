import datetime
import json

from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.text import slugify
from uri import URI
from urllib.request import urlopen
from .repositories import Repository


class Service(object):

    def verify_required_data(self, data: dict):
        for i in self.fields:
            if data.get(i) is None and self.fields[i].get('required') is True:
                raise ValueError(f'{i} must not be null')
            if self.fields.get(i).get('type') == 'foreign_key' and data.get(i) is not None:
                data[f'{i}_id'] = data.pop(i)
            elif self.fields.get('type') == 'many_to_many':
                try:
                    data[i] = Repository(model=self.fields.get('modelToMap')).retrieve_by_id(data[i])
                except self.fields.get('modelToMap').DoesNotExist:
                    raise ValueError(f'{i} with id = {data[i]} is not found')

            elif self.fields[i].get('type') == 'slug':
                if self.fields[i].get('field_to_slug') is None:
                    raise ValueError('field to slug must be not None')
                data[i] = slugify(data[self.fields[i].get('field_to_slug')])
            elif self.fields[i].get('unique') is True:
                try:
                    self.repository.retrieve({i: data.get(i)})
                    raise ValueError(f'{i} is unique')
                except self.repository.model.DoesNotExist:
                    continue
        return data

    def __init__(self, repository: Repository, fields: dict):
        self.repository = repository
        self.fields = fields

    def list(self):
        return self.repository.list()

    def retrieve(self, pk: int or str):
        try:
            return self.repository.retrieve_by_id(int(pk))
        except TypeError:
            return self.repository.retrieve({'slug': pk})

    def create(self, data: dict):
        self.verify_required_data(data)
        return self.repository.create(data)

    def put(self, pk: int, data: dict):
        return self.repository.put(pk=pk, data=data)

    def delete(self, pk: int):
        return self.repository.delete(pk)

    def filter_by(self, data: dict):
        filter_params = {}
        for i in data:
            if self.fields.get(i) is not None and self.fields.get(i).get('type') == 'text':
                filter_params[f'{i}__contains'] = data[i]
            filter_params[i] = data[i]
        return self.repository.filter_by(data=filter_params)

    def import_data(self, data: list):
        for row in data:
            instance_data = {}
            for i in self.fields:
                if self.fields[i].get('type') == 'file':
                    instance_data[i] = SimpleUploadedFile(name=str(URI(str(row[i])).path).split('/')[-1],
                                                          content=urlopen(url=str(data.get(i))).read())
                elif self.fields[i].get('type') == 'date' or self.fields[i].get('type') == 'datetime':
                    instance_data[i] = datetime.datetime.fromisoformat(data[i])
                elif self.fields[i].get('type') == 'foreign_key':
                    try:
                        instance_data[f'{i}_id'] = int(data.pop(i))
                    except ValueError:
                        instance, _ = self.fields.get(i).get('classMap').objects.get_or_create(**json.loads(str(
                            row.pop(i))))
                        instance_data[f'{i}_id'] = instance.id
                else:
                    instance_data[i] = str(row[i])
            self.create(instance_data)

    def export_data(self):
        output = {}
        data = self.repository.list()
        for row in data:
            for field in self.fields:
                if output.get(field) is None:
                    if self.fields.get(field).get('type') == 'int':
                        value = int(getattr(row, field))
                    elif self.fields.get(field).get('type') == 'float':
                        value = float(getattr(row, field))
                    elif self.fields.get(field).get('type') == 'file':
                        value = str(getattr(getattr(data, field), 'url'))
                    else:
                        value = str(getattr(row, field))
