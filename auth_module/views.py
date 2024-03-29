from django.db.models import Q

from .services import login, find_user_by_username_or_email, send_code, verify_code, signup
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR, \
    HTTP_204_NO_CONTENT, HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_201_CREATED
from django.contrib.auth.models import User
from crm.services import CustomerService
from django.urls import path


def generate_token_for_user(user):
    token = RefreshToken.for_user(user=user)
    return Response(data={
        "access": str(token.access_token),
        "refresh": str(token),
        "userId": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "is_superuser": user.is_superuser
    }, status=HTTP_200_OK)


# Create your views here.
@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny])
def login_view(request, *args, **kwargs):
    try:
        user = login({
            'username': request.data.get('username'),
            'password': request.data.get('password')
        })
        if user.is_superuser is False and user.customerprofile.has_two_factors_authentication:
            send_code(user.email)
            return Response(data={}, status=HTTP_200_OK)
        return generate_token_for_user(user)
    except (ValueError, User.DoesNotExist) as valueError:
        status = HTTP_404_NOT_FOUND if isinstance(valueError, User.DoesNotExist) else HTTP_400_BAD_REQUEST
        return Response(data={'message': str(valueError)}, status=status)


@csrf_exempt
@api_view(['POST'])
def verify_code_view(request, *args, **kwargs):
    try:
        verify_code(request.data.get('email'), int(request.data.get('code')))
        user = User.objects.find(email=request.data.get('email'))
        return generate_token_for_user(user)
    except Exception as exception:
        if isinstance(exception, ValueError):
            return Response(data={'message': 'wrong code'}, status=HTTP_401_UNAUTHORIZED)
        return Response(data={'message': str(exception)}, status=HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@csrf_exempt
def signup_view(request, *args, **kwargs):
    try:
        signup({
            'username': request.data.get('username'),
            'first_name': request.data.get('first_name'),
            'last_name': request.data.get('last_name'),
            'email': request.data.get('email'),
            'password': request.data.get('password'),
            'customerprofile': request.data.get('customerprofile')
        })
        return Response(status=HTTP_201_CREATED, data={})
    except Exception as exception:
        if isinstance(exception, ValueError):
            print(exception)
            return Response(data={'message': 'account already found'}, status=HTTP_400_BAD_REQUEST)
        return Response(data={'message': str(exception)}, status=HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def reset_password(request, *args, **kwargs):
    user = request.user if request.user.is_authenticated else find_user_by_username_or_email({'username': request.data.get('username')})
    if user is None:
        return Response(data={'message': 'user not found wirth the given username or email'}, status=HTTP_404_NOT_FOUND)
    user.set_password(request.data.get('password'))
    user.save()
    return Response(data={'message': 'password reset successfully'}, status=HTTP_200_OK)


@csrf_exempt
@api_view(http_method_names=['POST'])
def logout(request, *args, **kwargs):
    token = RefreshToken(request.data.get('refresh'))
    token.blacklist()
    return Response(status=HTTP_204_NO_CONTENT)

#
# @api_view(['GET', 'POST'])
# def forget_password(request, *args, **kwargs):
#

urlpatterns = [
    path('login', login_view),
    path('signup', signup_view),
    path('logout', logout),
    path('verify_code', verify_code_view),
    path('reset_password', reset_password)
]
