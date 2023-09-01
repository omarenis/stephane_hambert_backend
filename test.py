import os

import requests
from requests.auth import HTTPBasicAuth

client_id = "ATn0ffXhzXyEsGaezH4t4kIrGACJvOdt1CiuuAda3iypiwmqK8jaWFAMlgxlswxErhOZRlUqiKfh6hN-"
client_secret = "EJV-MWkDz78NAlW5JW9YcNFkxKJhTCZBYrg4ukDeUM5_gD-SJEULDwpcQZ197Adw5AnNXiVvlD0_D8gO"
from paypalpayoutssdk.core import PayPalHttpClient, SandboxEnvironment


class PayPalClient:
    def __init__(self):
        self.client_id = os.environ["PAYPAL-CLIENT-ID"] if 'PAYPAL-CLIENT-ID' in os.environ else client_id
        self.client_secret = os.environ[
            "PAYPAL-CLIENT-SECRET"] if 'PAYPAL_CLIENT_SECRET' in os.environ else client_secret
        self.environment = SandboxEnvironment(client_id=self.client_id, client_secret=self.client_secret)
        self.client = PayPalHttpClient(self.environment)


print(PayPalClient().client)

def get_access_token_and_token_type():
    request = requests.post(url="https://api-m.sandbox.paypal.com/v1/oauth2/token",
                            data={"grant_type": "client_credentials"},
                            headers={"Content-Type": "application/x-www-form-urlencoded"},
                            auth=HTTPBasicAuth(client_id, client_secret))
    response = dict(request.json())
    access_token = response.get('access_token')
    token_type = response.get('token_access')
    return {'access_token': access_token, 'token_type': token_type}


def payment_function():
    data = get_access_token_and_token_type()
    import requests
    headers = {
        'Content-Type': 'application/json',
        'PayPal-Request-Id': '7b92603e-77ed-4896-8e78-5dea2050476a',
        'Authorization': f'{data["token_type"]} {data["access_token"]}',
    }

    data = '{ "intent": "CAPTURE", "purchase_units": [ { "reference_id": "d9f80740-38f0-11e8-b467-0ed5f89f718b", "amount": { "currency_code": "USD", "value": "100.00" } } ], "payment_source": { "paypal": { "experience_context": { "payment_method_preference": "IMMEDIATE_PAYMENT_REQUIRED", "brand_name": "EXAMPLE INC", "locale": "en-US", "landing_page": "LOGIN", "shipping_preference": "SET_PROVIDED_ADDRESS", "user_action": "PAY_NOW", "return_url": "https://example.com/returnUrl", "cancel_url": "https://example.com/cancelUrl" } } } }'

    response = requests.post('https://api-m.sandbox.paypal.com/v2/checkout/orders', headers=headers, data=data)
    print(response.json())


payment_function()
