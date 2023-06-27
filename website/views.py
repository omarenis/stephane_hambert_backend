from django.core.mail import send_mail
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from stock_management.models import Product, Collection, ProductSerializer, CollectionSerializer
from website.models import Inscription


# Create your views here.
def index(request, *args, **kwargs):

    products = Product.objects.order_by('-price')[:8]
    collections = Collection.objects.all()
    return Response(data={
        "products": [ProductSerializer(product).data for product in products],
        "collections": [CollectionSerializer(collection).data for collection in collections]
    })


@api_view(['POST'])
def newsletter_inscription(request, *args, **kwargs):
    try:
        inscription = Inscription.objects.get(email=request.data.email)
        return Response(data={'message': 'inscription already exists'}, status=HTTP_400_BAD_REQUEST)
    except Inscription.DoesNotExist:
        send_mail()
        Inscription.objects.create(email=request.data.email)
