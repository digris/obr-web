# -*- coding: utf-8 -*-
import logging

from django.utils import timezone
from datetime import timedelta

from subscription.models import Subscription, SubscriptionType

from . import get_subscription


NUM_DAYS_TRIAL = 3


def get_options(user, num_days=NUM_DAYS_TRIAL):

    subscription = get_subscription(user=user)

    if subscription:
        return []

    options = [
        {
            "num_days": num_days,
            "until_date": timezone.now().date() + timedelta(days=num_days),
        },
    ]

    return options


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
