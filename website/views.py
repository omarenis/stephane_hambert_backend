from django.urls import path
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND

from common.repositories import Repository
from common.services import Service
from common.views import ViewSet
from website.models import Product, Collection, CollectionSerializer, Present, PresentSerializer
from stock_management.services import CategoryService, ProductService, CollectionService
from website.models import OlfactionSerializer, HistorySerializer, AdditionalInformationCollectionSerializer, \
    ProductPageModelSerializer, ProductListSerializer
from website.services import OlfactionService, HistoryService, OtherInformationForCollectionService


# Create your views here.
@api_view(['GET'])
def index(request, *args, **kwargs):
    data = {
        'products': None,
        'collections': None,
        'presents': None
    }
    products = None
    presents = None
    if request.GET.get('products') is None and request.GET.get('presents') is None:
        data['collections'] = Collection.objects.all()

    elif request.GET.get('product') == 'best_sellers':
        products = Product.objects.order_by('-number_purchases')
    else:
        data['products'] = Product.objects.all()

    if request.GET.get('presents'):
        data['presents'] = Present.objects.all()

    return Response(data={
        "products": [ProductListSerializer(product).data for product in data['products']],
        "collections": [CollectionSerializer(collection).data for collection in data['presents']]
    })


@api_view(['GET'])
def products_page_controller(request, *args, **kwargs):
    filter_products = {}
    print(request.GET.get('collection'))
    if request.GET.get('collection') is not None:
        filter_products = {'collection': int(request.GET.get('collection'))}
    print(ProductService().filter_by(filter_products))
    collections = [{"id": i.id, 'title': i.title} for i in CollectionService().list()]
    products = [ProductListSerializer(product).data for product in
                (ProductService().list() if filter_products == {} else ProductService().filter_by(filter_products))]
    print(products);
    return Response(data={
        "products": products,
        "collections": collections
    })


@api_view(['GET'])
def product_page_controller(request, slug: str, *args, **kwargs):
    product = ProductService().retrieve_by({'slug': slug})
    if product is None:
        return Response(data={'message': 'product not found'}, status=HTTP_404_NOT_FOUND)
    return Response(data=ProductPageModelSerializer(product).data, status=HTTP_200_OK)


@api_view(['GET'])
def collections_page_controller(request, *args, **kwargs):
    collections = Collection.objects.all()
    collections_data = [CollectionSerializer(collection).data for collection in collections]
    return Response(data=collections_data, status=HTTP_200_OK)


class OlfactionViewSet(ViewSet):

    def __init__(self, serializer_class=OlfactionSerializer, service=OlfactionService(), **kwargs):
        super().__init__(serializer_class, service, **kwargs)


class HistoryViewSet(ViewSet):

    def __init__(self, serializer_class=HistorySerializer, service=HistoryService(), **kwargs):
        super().__init__(serializer_class, service, **kwargs)


class OtherInformationCollectionViewSet(ViewSet):

    def __init__(self, serializer_class=AdditionalInformationCollectionSerializer,
                 service=OtherInformationForCollectionService(), **kwargs):
        super().__init__(serializer_class, service, **kwargs)


class PresentViewSet(ViewSet):

    def __init__(self, serializer_class=PresentSerializer, service=Service(repository=Repository(model=Present)),
                 **kwargs):
        super().__init__(serializer_class, service, **kwargs)


olfactions, olfaction = OlfactionViewSet.get_urls()
histories, history = HistoryViewSet.get_urls()
other_information_for_collection, other_information_for_collection_instance = OtherInformationCollectionViewSet.get_urls()
presents, present =  PresentViewSet.get_urls()

urlpatterns = [
    path('public/index', index),
    path('public/products', products_page_controller),
    path('public/collections', collections_page_controller),
    path('public/products/<str:slug>', product_page_controller),
    path('stock-management/other-information-for-collection', other_information_for_collection),
    path('stock-management/other-information-for-collection/<int:pk>', other_information_for_collection_instance),
    path('stock-management/olfactions', olfactions),
    path('stock-management/olfactions/<int:pk>', olfaction),
    path('stock-management/histories', histories),
    path('stock-management/histories/<int:pk>', history),
    path('cms/presents', presents),
    path('cms/presents/<int:pk>', present),
]
