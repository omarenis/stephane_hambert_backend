from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Inscription


# Create your views here.
@api_view(['POST'])
def create_inscription(request, *args, **kwargs):
    try:
        Inscription.objects.get(email=request.data.get('email'))
        return Response(data={'message': 'email already exists in our newsletter subscription'})
    except Inscription.DoesNotExist:
        Inscription.objects.create(email=request.data.get('email'))
        return Response(data={'message': 'email successfully added to newsletter subscription'})


