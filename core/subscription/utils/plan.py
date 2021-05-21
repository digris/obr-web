# -*- coding: utf-8 -*-
import logging
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta

from subscription.models import Subscription, SubscriptionType
from subscription.utils import get_subscription

logger = logging.getLogger(__name__)

PLANS = [
    {
        "sku": "OBR-P-M1",
        "title": "1 Monat",
        "price": Decimal(0.99),
        "num_days": 28,
    },
    {
        "sku": "OBR-P-M3",
        "title": "3 Monate",
        "price": Decimal(3),
        "num_days": 85,
    },
    {
        "sku": "OBR-P-M6",
        "title": "6 Monate",
        "price": Decimal(6),
        "num_days": 183,
    },
    {
        "sku": "OBR-P-M12",
        "title": "1 Jahr",
        "price": Decimal(10),
        "num_days": 365,
    },
]


def get_plan_by_sku(sku):
    return next((p for p in PLANS if p["sku"] == sku), None)


def get_options(user):

    subscription = get_subscription(user=user)

    if subscription and subscription.is_active:
        from_date = subscription.active_until.date()
    else:
        from_date = timezone.now().date()

    for plan in PLANS:
        option = plan.copy()
        option.update(
            {
                "until_date": from_date + timedelta(days=option["num_days"]),
            }
        )
        yield option

    return []


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
