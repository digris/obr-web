import re

from datetime import timedelta

from django.utils import timezone
from django.db import transaction

from subscription.models import Voucher, Redemption
from subscription.utils import get_subscription, extend_subscription


class VoucherValidationException(Exception):
    pass


def validate_code(code):
    return re.match(r"^[A-Z]{6}$", code) is not None


def get_until_date(subscription, num_days):

    if subscription and subscription.is_active:
        from_date = subscription.active_until.date()
    else:
        from_date = timezone.now().date()

    return from_date + timedelta(days=num_days)


def get_voucher(user, code):

    if not validate_code(code):
        raise VoucherValidationException("Malformatted code")

    qs = Voucher.objects.filter(code=code)

    if not qs.exists():
        raise VoucherValidationException("Code does not exist")

    voucher = qs.first()

    if (
        user.is_authenticated
        and Redemption.objects.filter(voucher=voucher, user=user).exists()
    ):
        raise VoucherValidationException("Code already used")

    subscription = get_subscription(user=user)

    voucher.is_valid_for_user = True
    voucher.until_date = get_until_date(
        subscription=subscription,
        num_days=voucher.num_days,
    )

    return voucher


@transaction.atomic
def redeem_voucher(user, code):
    voucher = get_voucher(user, code)
    redemption = Redemption(voucher=voucher, user=user)
    redemption.save()
    extend_subscription(user=user, num_days=voucher.num_days)
    return True
