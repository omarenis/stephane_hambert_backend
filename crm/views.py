from common.views import ViewSet, extract_get_data, extract_serialized_objects_response
from crm.models import UserSerializer
from crm.services import CustomerService
from django.urls import path


# Create your views here.
class CustomerViewSet(ViewSet):

    def __init__(self, serializer_class=UserSerializer, service=CustomerService(), **kwargs):
        super().__init__(serializer_class, service, **kwargs)


customers, customer = CustomerViewSet.get_urls()

urlpatterns = [
    path('customers', customers),
    path('customers/<int:pk>', customer)
]
