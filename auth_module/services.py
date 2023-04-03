import json

from django.contrib.auth.models import User
from requests import post
from rest_framework.status import HTTP_200_OK
from backend.settings import CLIEND_ID, CLIENT_SECRET, DOMAIN
from django.core.validators import validate_email, ValidationError
from crm.services import CustomerService

# def login(data: dict):
#     user = User.objects.get(email=data.get('email'))
#     if user.is_superuser is False:
#


def send_code(email):
    response = post(f"{DOMAIN}/passwordless/start", data={
        'client_id': CLIEND_ID,
        'client_secret': CLIENT_SECRET,
        'connection': 'email',
        'send': 'code',
        'email': email
    })
    if response.status_code == HTTP_200_OK:
        return json.loads(response.text)
    raise ValidationError('bad email or service corrupted, please check your email first')


def find_user_by_username_or_email(data):
    try:
        validate_email(data.get('username'))
        data['email'] = data.pop('username')
    except ValidationError:
        pass

    try:
        return User.objects.get(**data)
    except User.DoesNotExist:
        return None


def login(data: dict):
    password = data.pop('password')
    try:
        validate_email(data.get('username'))
        data['email'] = data.pop('username')
    except ValidationError:
        pass
    try:
        user = User.objects.get(**data)
        if user.check_password(password):
            return user
        raise ValueError('password did not match')
    except User.DoesNotExist:
        raise User.DoesNotExist('user with username or email not found')


def signup(data: dict):
    user = find_user_by_username_or_email({'username': data.get('username')})
    if user is None:
        user = CustomerService().create(data=data)
        send_code(user.email)
    else:
        raise ValueError('user with username or email exists')
    return user


def verify_code(email, code):
    response = json.loads(post(f'{DOMAIN}/oauth/token', data={
        "grant_type": "http://auth0.com/oauth/grant-type/passwordless/otp",
        'client_id': CLIEND_ID,
        'client_secret': CLIENT_SECRET,
        'otp': code,
        'realm': 'email',
        'username': email
    }).text)
    print(response)
    if response.get('error') is not None:
        raise ValueError(response.get('error_description'))
    return response
