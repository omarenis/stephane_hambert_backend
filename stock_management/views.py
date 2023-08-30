from django.urls import path
from common.views import ViewSet
from stock_management.models import ProductSerializer, CategorySerializer, PromoSerializer, CollectionSerializer, \
    ProductListSerializer
from stock_management.services import ProductService, PromoService, CategoryService, CollectionService


# Create your views here.
class ProductViewSet(ViewSet):

    def __init__(self, serializer_class=ProductSerializer, service=ProductService(), **kwargs):
        super().__init__(serializer_class, service, **kwargs)

    def list(self, request, *args, **kwargs):
        self.serializer_class = ProductListSerializer
        return super().list(request)


class CollectionViewSet(ViewSet):

    def __init__(self, serializer_class=CollectionSerializer, service=CollectionService(), **kwargs):
        super().__init__(serializer_class, service, **kwargs)


class CategoryViewSet(ViewSet):
    def __init__(self, serializer_class=CategorySerializer, service=CategoryService(), **kwargs):
        super().__init__(serializer_class, service, **kwargs)


class PromoteViewSet(ViewSet):
    def __init__(self, serializer_class=PromoSerializer, service=PromoService(), **kwargs):
        super().__init__(serializer_class, service, **kwargs)


products, product = ProductViewSet.get_urls()
categories, category = CategoryViewSet.get_urls()
promos, promo = PromoteViewSet.get_urls()
collections, collection = CollectionViewSet.get_urls()
urlpatterns = [
    path('products', products),
    path('products/<int:pk>', product),
    path('categories', categories),
    path('categories/<int:pk>', category),
    path('promos', promos),
    path('promos/<int:pk>', promo),
    path('collections', collections),
    path('collections/<int:pk>', collection)
]
