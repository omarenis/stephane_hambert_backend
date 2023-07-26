from common.repositories import Repository
from common.services import Service
from website.models import AdditionalInformation

ADDITIONAL_INFORMATION = {
    'type_information': {'tpye': 'text', 'required': True},
    'image': {'type': 'file', 'required': True},
    'description': {'type': 'text', 'required': True},
    'title': {'type': 'text', 'required': True},
    'product': {'type': 'foreign_key', 'required': True}
}


class AdditionalInformationService(Service):

    def __init__(self, repository: Repository = Repository(model=AdditionalInformation)):
        super().__init__(repository, ADDITIONAL_INFORMATION)
