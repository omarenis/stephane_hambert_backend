from newsletter.models import Subscription


def create_subscription(email):
    try:
        Subscription.objects.get(email=email)
        raise ValueError('email already exists in our newsletter subscription')
    except Subscription.DoesNotExist:
        return Subscription.objects.create(email=email)


def delete_subscription(pk):
    try:
        Subscription.objects.get(id=pk).delete()
    except Subscription.DoesNotExist:
        raise Subscription.DoesNotExist('subscription does not exist ')
