import json

from django.contrib.auth.models import User
from requests import post
from rest_framework.status import HTTP_200_OK
from backend.settings import CLIEND_ID, CLIENT_SECRET, DOMAIN
from django.core.validators import validate_email, ValidationError

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
    raise Exception('bad request or invalid code')


def verify_code(email, code):
    response = json.loads(post(f'{DOMAIN}/oauth/token', data={
        "grant_type": "http://auth0.com/oauth/grant-type/passwordless/otp",
        'client_id': CLIEND_ID,
        'client_secret': CLIENT_SECRET,
        'otp': code,
        'realm': 'email',
        'username': email
    }).text)
    if response.get('access_token') is None:
        raise ValueError(response.get('message'))
    return response


def find_user_by_username(data):
    try:
        validate_email(data.get('username'))
        data['email'] = data.pop('username')
    except ValidationError:
        pass

    try:
        return User.objects.get(**data)
    except User.DoesNotExist:
        return None

def login(data):
    user = find_user_by_username({'username': data.get('username')})
    if user is None:
        user = User()
        user.first_name = data.get('first_name')
        user.last_name = data.get('last_name')
        user.phone = data.get('phone')

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
        raise ValueError('user with username or email not found')


def signup(data: dict):
