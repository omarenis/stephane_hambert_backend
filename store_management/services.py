from common.repositories import Repository
from common.services import Service
from store_management.models import Store, Localisation

STORE_FIELDS = {
    'label': {'type': 'string', 'required': True},
    'localisation': {'type': 'foreign_key', 'required': True, 'classMap': Localisation},
    'image': {'type': 'file', 'required': True},
    'number_products': {'type': 'int', 'required': False},
    'promo': {'type': 'foreign_key', 'required': False}
}

class StoreService(Service):

    def __init__(self, repository: Repository=Repository(model=Store), fields=None):
        if fields is None:
            fields = STORE_FIELDS
        super().__init__(repository, fields)
