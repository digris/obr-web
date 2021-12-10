from datetime import timedelta

from django.utils import timezone

from subscription.models import Subscription, SubscriptionType

NUM_DAYS_TRIAL = 3


def start_trial(user, num_days=NUM_DAYS_TRIAL):

    num_seconds = 60 * 60 * 24 * (num_days + 1)
    today = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
    active_until = today + timedelta(seconds=num_seconds - 1)

    subscription = Subscription.objects.create(
        user=user,
        type=SubscriptionType.TRIAL,
        active_until=active_until,
    )

    return subscription
