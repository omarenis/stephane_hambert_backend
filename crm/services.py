from common.repositories import Repository
from common.services import Service
from django.contrib.auth.models import User

from crm.models import CustomerProfile

USER_FIELDS = {
    'username': {'type': 'string', 'required': True},
    'first_name': {'type': 'string', 'required': True},
    'last_name': {'type': 'string', 'required': True},
    'email': {'type': 'string', 'required': True},
    'password': {'type': 'string', 'required': True}
}

CUSTOMER_FIELDS = {
    'user': {'type': 'foreign_key', 'required': True},
    'facebook': {'type': 'string', 'required': False},
    'google': {'type': 'string', 'required': False},
    'phone': {'type': 'string', 'required': True},
    'gender': {'type': 'text', 'required': True}
}


class CustomerService(Service):

    def __init__(self, repository=Repository(model=User), fields=None):
        if fields is None:
            fields = USER_FIELDS

        super().__init__(repository, fields)
        self.fields.update(CUSTOMER_FIELDS)
        self.customer_repository = Repository(model=CustomerProfile)

    def create(self, data: dict):
        try:
            User.objects.get(username=data.get('username'))
            raise ValueError('user found with given username')
        except User.DoesNotExist:
            try:
                User.objects.get(email=data.get('email'))
                raise ValueError('user found with given email')
            except User.DoesNotExist:
                self.verify_required_data(data)
                user = User.objects.create(
                    username=data.get('username'),
                    first_name=data.get('first_name'),
                    last_name=data.get('last_name'),
                    email=data.get('email')
                )
                user.set_password(raw_password=data.get('password'))
                user.save()
                self.customer_repository.create({
                    'user': user,
                    'facebook': data.get('facebook'),
                    'google': data.get('google'),
                    'phone': data.get('phone'),
                    'gender': data.get('gender')
                })
                return user
