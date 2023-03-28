from django.shortcuts import render
from django.urls import path

from common.views import ViewSet
from stock_management.models import ProductSerializer, CategorySerializer, PromoSerializer
from stock_management.services import ProductService, PromoService, CategoryService


# Create your views here.
class ProductViewSet(ViewSet):

    def __init__(self, serializer_class=ProductSerializer, service=ProductService(), **kwargs):
        super().__init__(serializer_class, service, **kwargs)


class CategoryViewSet(ViewSet):
    def __init__(self, serializer_class=CategorySerializer, service=CategoryService(), **kwargs):
        super().__init__(serializer_class, service, **kwargs)


class PromoteViewSet(ViewSet):
    def __init__(self, serializer_class, service, **kwargs):
        super().__init__(serializer_class, service, **kwargs)


class BrandViewSet(ViewSet):
    def __init__(self, serializer_class=PromoSerializer, service=PromoService(), **kwargs):
        super().__init__(serializer_class, service, **kwargs)


products, product = ProductViewSet.get_urls()
categories, category = CategoryViewSet.get_urls()
brands, brand = BrandViewSet.get_urls()
promos, promo = PromoteViewSet.get_urls()

urlpatterns = [
    path('products', products),
    path('products/<int:pk>', product),
    path('categories', categories),
    path('categories/<int:pk>', category),
    path('brands', brands),
    path('brands/<int:pk>', brand),
    path('promos', brands),
    path('promos/<int:pk>', brand),
]
