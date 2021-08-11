# -*- coding: utf-8 -*-
import logging
from datetime import timedelta
from django.utils import timezone

from subscription.models import Subscription, SubscriptionType

logger = logging.getLogger(__name__)


def get_subscription(user):
    if not user.is_authenticated:
        return None
    try:
        return Subscription.objects.get(user=user)
    except Subscription.DoesNotExist:
        return None


def extend_subscription(user, num_days):
    logger.info(f"extend subscription for {user} by {num_days} days.")
    subscription = get_subscription(user=user)

    t_delta = timedelta(days=num_days + 1, seconds=-1)

    if not subscription:
        subscription = Subscription.objects.create(
            user=user,
            active_until=timezone.now().date() + t_delta,
            type=SubscriptionType.PLAN,
        )
        return subscription

    if subscription.is_active:
        subscription.active_until += t_delta

    else:
        subscription.active_until = timezone.now().date() + t_delta

    subscription.type = SubscriptionType.PLAN
    subscription.save()

    return subscription
