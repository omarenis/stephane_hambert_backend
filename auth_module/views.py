from .services import login, find_user_by_username_or_email, send_code, verify_code, signup
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR, \
    HTTP_204_NO_CONTENT, HTTP_200_OK, HTTP_401_UNAUTHORIZED
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
            'facebook': request.data.get('facebook'),
            'google': request.data.get('google'),
            'phone': request.data.get('phone'),
            'gender': request.data.get('gender')
        })
        return Response(status=HTTP_204_NO_CONTENT)
    except Exception as exception:
        if isinstance(exception, ValueError):
            return Response(data={'message': 'account already found'}, status=HTTP_400_BAD_REQUEST)
        return Response(data={'message': str(exception)}, status=HTTP_500_INTERNAL_SERVER_ERROR)


urlpatterns = [
    path('login', login_view),
    path('signup', signup_view),
    path('verify_code', verify_code_view)
]
