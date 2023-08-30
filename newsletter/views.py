from django.core.mail import send_mail
from django.urls import path
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from .models import Subscription, SubscriptionSerializer
from .services import delete_subscription

@api_view(['GET', 'POST'])
def get_inscriptions(request, *args, **kwargs):
    if request.method == 'POST':
        try:
            Subscription.objects.get(email=request.data.get('email'))
            return Response(data={'message': 'email already exists in our newsletter subscription'})
        except Subscription.DoesNotExist:
            Subscription.objects.create(email=request.data.get('email'))
            return Response(data={'message': 'email successfully added to newsletter subscription'})

    return Response(data=[SubscriptionSerializer(i).data for i in Subscription.objects.all()], status=HTTP_200_OK)


@api_view(['DELETE'])
def delete_subscription_view(request, pk=None, *args, **kwargs):
    try:
        delete_subscription(pk=pk)
    except Subscription.DoesNotExist:
        return Response(data={'message': 'subscription not found'}, status=HTTP_404_NOT_FOUND)


urlpatterns = [
    path('subscriptions', get_inscriptions),
    path('subsciptions/<int:pk>', delete_subscription_view)
]
