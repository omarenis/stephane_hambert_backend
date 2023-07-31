from common.repositories import Repository
from common.services import Service
from website.models import OlfactiveProduct, History

ADDITIONAL_INFORMATION = {
    'image': {'type': 'file', 'required': True},
    'description': {'type': 'text', 'required': True},
    'title': {'type': 'text', 'required': True},
}

ADDITIONAL_INFORMATION_PRODUCT = {
    **ADDITIONAL_INFORMATION,
    'product': {'type': 'one_to_one', 'required': True}
}

ADDITIONAL_INFORMATION_COLLECTION = {
    **ADDITIONAL_INFORMATION,
    'collection': {'type': 'one_to_one', 'required': True}
}


HISTORY_FIELDS = {
    'image': {'type': 'file', 'required': True},
    'description': {'type': 'text', 'required': True},
    'title': {'type': 'text', 'required': True},
    'product': {'type': 'one_to_one', 'required': True}
}


class OlfactiveService(Service):

    def __init__(self, repository: Repository = Repository(model=Olfactive)):
        super().__init__(repository, ADDITIONAL_INFORMATION)


class HistoryService(Service):

    def __init__(self, repository=Repository(model=History), fields=HISTORY_FIELDS):
        super().__init__(Repository, fields=fields)
