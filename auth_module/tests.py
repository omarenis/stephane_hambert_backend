import json
import requests
from django.test import TestCase
from authlib.oauth1.client import OAuth1Client

from auth_module.services import send_code, verify_code
from backend.settings import CLIEND_ID, CLIENT_SECRET


# Create your tests here.
class AuthTest(TestCase):

    def setUp(self) -> None:
        self.valid_email = 'omartriki712@gmail.com'
        self.invalid_email  = 'omar@example.com'

    def test_reset_password(self):

        response = send_code(email=self.valid_email)
        print(type(response))

    def test_verify_code(self):
        response = verify_code(email=self.valid_email, code=984820)
        print(response.text)
