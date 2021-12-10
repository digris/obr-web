import logging
from datetime import timedelta
from decimal import Decimal

from django.utils import timezone

from subscription.utils import get_subscription

logger = logging.getLogger(__name__)

PLANS = [
    {
        "sku": "OBR-P-M1",
        "title": "+ 1 Monat",
        "price": Decimal(1),
        "num_days": 31,
    },
    {
        "sku": "OBR-P-M3",
        "title": "+ 3 Monate",
        "price": Decimal(3),
        "num_days": 93,
    },
    {
        "sku": "OBR-P-M6",
        "title": "+ 6 Monate",
        "price": Decimal(6),
        "num_days": 186,
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
