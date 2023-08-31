import requests
from requests.auth import HTTPBasicAuth

client_id = "ATn0ffXhzXyEsGaezH4t4kIrGACJvOdt1CiuuAda3iypiwmqK8jaWFAMlgxlswxErhOZRlUqiKfh6hN-"
client_secret = "EJV-MWkDz78NAlW5JW9YcNFkxKJhTCZBYrg4ukDeUM5_gD-SJEULDwpcQZ197Adw5AnNXiVvlD0_D8gO"


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
    import requests

    headers = {
        'X-PAYPAL-SECURITY-CONTEXT': '{"actor":{"account_number":"1659371090107732880","party_id":"1659371090107732880","auth_claims":["AUTHORIZATION_CODE"],"auth_state":"ANONYMOUS","client_id":"zf3..4BQ0T9aw-ngFr9dmOUZMwuKocrqe72Zx9D-Lf4"},"auth_token":"A015QQVR4S3u79k.UvhQ-AP4EhQikqOogdx-wIbvcvZ7Qaw","auth_token_type":"ACCESS_TOKEN","last_validated":1393560555,"scopes":["https://api-m.sandbox.paypal.com/v1/payments/.*","https://api-m.sandbox.paypal.com/v1/vault/credit-card/.*","openid","https://uri.paypal.com/services/payments/futurepayments","https://api-m.sandbox.paypal.com/v1/vault/credit-card","https://api-m.sandbox.paypal.com/v1/payments/.*"],"subjects":[{"subject":{"account_number":"2245934915437588879","party_id":"2245934915437588879","auth_claims":["PASSWORD"],"auth_state":"LOGGEDIN"}}]}',
    }

    data = '{ "intent": "sale", "payer": { "payment_method": "paypal" }, "transactions": [ { "amount": { "total": "30.11", "currency": "USD", "details": { "subtotal": "30.00", "tax": "0.07", "shipping": "0.03", "handling_fee": "1.00", "shipping_discount": "-1.00", "insurance": "0.01" } }, "description": "The payment transaction description.", "custom": "EBAY_EMS_90048630024435", "invoice_number": "48787589673", "payment_options": { "allowed_payment_method": "INSTANT_FUNDING_SOURCE" }, "soft_descriptor": "ECHI5786786", "item_list": { "items": [ { "name": "hat", "description": "Brown hat.", "quantity": "5", "price": "3", "tax": "0.01", "sku": "1", "currency": "USD" }, { "name": "handbag", "description": "Black handbag.", "quantity": "1", "price": "15", "tax": "0.02", "sku": "product34", "currency": "USD" } ], "shipping_address": { "recipient_name": "Brian Robinson", "line1": "4th Floor", "line2": "Unit #34", "city": "San Jose", "country_code": "US", "postal_code": "95131", "phone": "011862212345678", "state": "CA" } } } ], "note_to_payer": "Contact us for any questions on your order.", "redirect_urls": { "return_url": "https://example.com/return", "cancel_url": "https://example.com/cancel" } }'

    response = requests.post('https://api-m.sandbox.paypal.com/v1/payments/payment', headers=headers, data=data)
    print(response.json())


payment_function()
