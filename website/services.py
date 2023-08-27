from common.repositories import Repository
from common.services import Service
from stock_management.models import Collection
from website.models import History, Olfaction, AdditionalFile, AdditionalInformationCollection

ADDITIONAL_INFORMATION = {
    'image': {'type': 'file', 'required': True},
    'content': {'type': 'text', 'required': True},
    'title': {'type': 'text', 'required': True},
}

ADDITIONAL_INFORMATION_PRODUCT = {
    **ADDITIONAL_INFORMATION,
    'product': {'type': 'one_to_one', 'required': True}
}

HISTORY_FIELDS = {
    **ADDITIONAL_INFORMATION,
    'product': {'type': 'one_to_one', 'required': True}
}

ADDITIONAL_FILE_FIELD = {
    'image_or_video': {'type': 'file', 'required': True},
    'product': {'type': 'foreign_key', 'required': True}
}


OTHER_INFORMATION_FOR_COLLECTION = {
    'title': {'type': 'string', 'required': True, 'unique': True},
    'content': {'type': 'string', 'required': True},
    'image': {'type': 'image', 'required': True},
    'collection': {'type': 'foreign_key', 'required': True, 'classMap': Collection}
}

class OlfactionService(Service):

    def __init__(self, repository: Repository = Repository(model=Olfaction)):
        super().__init__(repository, ADDITIONAL_INFORMATION)


class HistoryService(Service):

    def __init__(self, repository=Repository(model=History), fields=None):
        if fields is None:
            fields = HISTORY_FIELDS
        super().__init__(repository=repository, fields=fields)


class AdditionAlFileService(Service):

    def __init__(self, repository: Repository = Repository(model=AdditionalFile)):
        super().__init__(repository, fields=ADDITIONAL_FILE_FIELD)


class OtherInformationForCollectionService(Service):

    def __init__(self, repository: Repository = Repository(model=AdditionalInformationCollection)):
        super().__init__(repository, fields=OTHER_INFORMATION_FOR_COLLECTION)
