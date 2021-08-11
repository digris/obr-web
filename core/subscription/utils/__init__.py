from subscription.models import Subscription


def get_subscription(user):
    if not user.is_authenticated:
        return None
    try:
        return Subscription.objects.get(user=user)
    except Subscription.DoesNotExist:
        return None
