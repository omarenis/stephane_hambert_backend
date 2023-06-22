from .repositories import Repository


class Service(object):

    def verify_required_data(self, data: dict):
        for i in self.fields:
            if data.get(i) is None and self.fields[i].get('required') is True:
                raise ValueError(f'{i} must not be null')
            if data.get('i').get('type') == 'foreign_key' and data.get(i) is not None:
                data[f'{i}_id'] = data.pop(i)
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

    def retrieve(self, pk: int):
        return self.repository.retrieve_by_id(pk=pk)

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
