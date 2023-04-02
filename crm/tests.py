from django.test import TestCase
from django.contrib.auth.models import User
from crm.models import UserSerializer, CustomerSerializer
from crm.services import CustomerService


class CustomerServiceTestCase(TestCase):

    def setUp(self) -> None:
        self.customerService = CustomerService()
        self.user_serializer = UserSerializer
        self.customer_serializer = CustomerSerializer

    def test_create_customer(self):
        data = {
            'username': 'omar',
            'email': 'omartriki712@gmail.com',
            'password': 'omar1996@+=',
            'first_name': 'omar',
            'last_name': 'triki',
            'phone': '+21624127616',
            'facebook': None,
            'google': None,
        }

        user = self.customerService.create(data)
        print(self.customer_serializer(user.customerprofile).data)
        self.assertIsInstance(user, User)
