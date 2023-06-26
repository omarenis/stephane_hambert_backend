from django.shortcuts import render
from rest_framework.response import Response

from stock_management.models import Product, Collection, ProductSerializer, CollectionSerializer


# Create your views here.
def index(request, *args, **kwargs):

    products = Product.objects.order_by('-price')
    collections = Collection.objects.all()
    return Response(data={
        "products": [ProductSerializer(product).data for product in products],
        "collections": [CollectionSerializer(collection).data for collection in collections]
    })
