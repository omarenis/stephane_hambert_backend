from django.test import TestCase
from auth_module.services import send_code, verify_code, signup


# Create your tests here.
class AuthTest(TestCase):

    def setUp(self) -> None:
        self.valid_email = 'omartriki712@gmail.com'
        self.invalid_email = 'omar@example.com'

    def test_reset_password(self):
        response = send_code(email=self.valid_email)
        print(type(response))

    def test_verify_code(self):
        response = verify_code(email=self.valid_email, code=612713)
        print(response.text)

    def test_signup(self):
        data = {
            "username": "@omartriki712",
            "email": "omartriki712@gmail.com",
            "password": "omartriki712@+=",
            "customerprofile": {
                "first_name": "triki",
                "last_name": "omar",
                "facebook": None,
                "google": "omartriki712@gmail.com",
                "phone": "+21624127616"
            }
        }
        user = signup(data=data)
        print(user)
