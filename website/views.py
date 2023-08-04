from django.core.mail import send_mail
from django.shortcuts import render
from django.urls import path
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from stock_management.models import Product, Collection, ProductSerializer, CollectionSerializer
from stock_management.services import CategoryService, ProductService
from website.models import Inscription


# Create your views here.
@api_view(['GET'])
def index(request, *args, **kwargs):
    products = Product.objects.order_by('-number_purchases')[:8]
    collections = Collection.objects.all()
    return Response(data={
        "products": [ProductSerializer(product).data for product in products],
        "collections": [CollectionSerializer(collection).data for collection in collections]
    })


@api_view(['GET'])
def products_page_controller(request, *args, **kwargs):
    categories = [{"id": i.id, 'label': i.label} for i in CategoryService().list()]
    products = [{
        "slug": product.slug
    } for product in ProductService().list()]


@api_view(['GET'])
def collections_page_controller():
    collections = Collection.objects.all()


urlpatterns = [
    path('index', index),
    path('products', products_page_controller)
]
