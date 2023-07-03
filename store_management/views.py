from django.shortcuts import render

from common.views import ViewSet


# Create your views here.


class StoreViewSet(ViewSet):

    def __init__(self, serializer_class=Store, service, **kwargs):
        super().__init__(serializer_class, service, **kwargs)
