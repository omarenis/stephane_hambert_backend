import os
import pathlib

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

def generate_invoice():

    data = get_access_token_and_token_type()
    headers = {
        'Authorization': f'{ data["token_type"] } { data["access_token"] }',
        'Content-Type': 'application/json',
        'Prefer': 'return=representation',
    }

    data = '{ "detail": { "invoice_number": "#123", "reference": "deal-ref", "invoice_date": "2018-11-12", "currency_code": "USD", "note": "Thank you for your business.", "term": "No refunds after 30 days.", "memo": "This is a long contract", "payment_term": { "term_type": "NET_10", "due_date": "2018-11-22" } }, "invoicer": { "name": { "given_name": "David", "surname": "Larusso" }, "address": { "address_line_1": "1234 First Street", "address_line_2": "337673 Hillside Court", "admin_area_2": "Anytown", "admin_area_1": "CA", "postal_code": "98765", "country_code": "US" }, "email_address": "merchant@example.com", "phones": [ { "country_code": "001", "national_number": "4085551234", "phone_type": "MOBILE" } ], "website": "www.test.com", "tax_id": "ABcNkWSfb5ICTt73nD3QON1fnnpgNKBy- Jb5SeuGj185MNNw6g", "logo_url": "https://example.com/logo.PNG", "additional_notes": "2-4" }, "primary_recipients": [ { "billing_info": { "name": { "given_name": "Stephanie", "surname": "Meyers" }, "address": { "address_line_1": "1234 Main Street", "admin_area_2": "Anytown", "admin_area_1": "CA", "postal_code": "98765", "country_code": "US" }, "email_address": "bill-me@example.com", "phones": [ { "country_code": "001", "national_number": "4884551234", "phone_type": "HOME" } ], "additional_info_value": "add-info" }, "shipping_info": { "name": { "given_name": "Stephanie", "surname": "Meyers" }, "address": { "address_line_1": "1234 Main Street", "admin_area_2": "Anytown", "admin_area_1": "CA", "postal_code": "98765", "country_code": "US" } } } ], "items": [ { "name": "Yoga Mat", "description": "Elastic mat to practice yoga.", "quantity": "1", "unit_amount": { "currency_code": "USD", "value": "50.00" }, "tax": { "name": "Sales Tax", "percent": "7.25" }, "discount": { "percent": "5" }, "unit_of_measure": "QUANTITY" }, { "name": "Yoga t-shirt", "quantity": "1", "unit_amount": { "currency_code": "USD", "value": "10.00" }, "tax": { "name": "Sales Tax", "percent": "7.25" }, "discount": { "amount": { "currency_code": "USD", "value": "5.00" } }, "unit_of_measure": "QUANTITY" } ], "configuration": { "partial_payment": { "allow_partial_payment": true, "minimum_amount_due": { "currency_code": "USD", "value": "20.00" } }, "allow_tip": true, "tax_calculated_after_discount": true, "tax_inclusive": false, "template_id": "TEMP-19V05281TU309413B" }, "amount": { "breakdown": { "custom": { "label": "Packing Charges", "amount": { "currency_code": "USD", "value": "10.00" } }, "shipping": { "amount": { "currency_code": "USD", "value": "10.00" }, "tax": { "name": "Sales Tax", "percent": "7.25" } }, "discount": { "invoice_discount": { "percent": "5" } } } } }'

    response = requests.post('https://api-m.sandbox.paypal.com/v2/invoicing/invoices', headers=headers, data=data)
    print(response)


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


generate_invoice()
