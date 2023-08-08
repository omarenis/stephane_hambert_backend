from django.urls import path
from common.views import ViewSet
from store_management.models import StoreSerializer
from store_management.services import StoreService


# Create your views here.


class StoreViewSet(ViewSet):

    def __init__(self, serializer_class=StoreSerializer(), service=StoreService(), **kwargs):
        super().__init__(serializer_class, service, **kwargs)


stores, store = StoreViewSet.get_urls()

urlpatterns = [
    path('stotres', stores),
    path('stores/:id', store)
]
