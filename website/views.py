from django.urls import path
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from common.views import ViewSet
from stock_management.models import Product, Collection, ProductSerializer, CollectionSerializer
from stock_management.services import CategoryService, ProductService
from website.models import OlfactionSerializer, HistorySerializer, AdditionalInformationCollectionSerializer
from website.services import OlfactionService, HistoryService, OtherInformationForCollectionService


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
        "slug": product.slug,
        "title": product.title,
        "price": product.price,
        "collection": product.collection
    } for product in ProductService().list()]
    return Response(data={
        "products": products,
        "categories": categories
    })


@api_view(['GET'])
def collections_page_controller():
    collections = Collection.objects.all()
    collections_data = [CollectionSerializer(collection).data for  collection in collections]
    return Response(data=collections_data, status=HTTP_200_OK)

class OlfactionViewSet(ViewSet):

    def __init__(self, serializer_class=OlfactionSerializer, service=OlfactionService(), **kwargs):
        super().__init__(serializer_class, service, **kwargs)


class HistoryViewSet(ViewSet):

    def __init__(self, serializer_class=HistorySerializer, service=HistoryService(), **kwargs):
        super().__init__(serializer_class, service, **kwargs)


class OtherInformationCollectionViewSet(ViewSet):

    def __init__(self, serializer_class=AdditionalInformationCollectionSerializer, service=OtherInformationForCollectionService(), **kwargs):
        super().__init__(serializer_class, service, **kwargs)


olfactions, olfaction = OlfactionViewSet.get_urls()
histories, history = HistoryViewSet.get_urls()
other_information_for_collection, other_information_for_collection_instance = OtherInformationCollectionViewSet.get_urls()

urlpatterns = [
    path('public/index', index),
    path('public/products', products_page_controller),
    path('public/collections', collections_page_controller),
    path('stock-management/other-information-for-collection', other_information_for_collection),
    path('stock-management/other-information-for-collection/<int:pk>', other_information_for_collection),
    path('stock-management/olfactions', olfactions),
    path('stock-management/olfactions/<int:pk>', olfaction),
    path('stock-management/histories', olfactions),
    path('stock-management/histories/<int:pk>', olfaction)
]
