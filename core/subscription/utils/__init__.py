from subscription.models import Subscription


def get_subscription(user):
    try:
        return Subscription.objects.get(user=user)
    except Subscription.DoesNotExist:
        return None
