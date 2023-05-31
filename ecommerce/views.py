from django.shortcuts import render
from django.urls import path

from common.views import ViewSet
from ecommerce.models import OrderSerializer
from ecommerce.service import OrderService


# Create your views here.

class OrderViewSet(ViewSet):

    def __init__(self, serializer_class=OrderSerializer, service=OrderService(), **kwargs):
        super().__init__(serializer_class, service, **kwargs)

orders, order = OrderViewSet.get_urls()

urlpatterns = [
    path('orders', orders),
    path('orders/<int:pk>', order)
]
