# -*- coding: utf-8 -*-
import re

from datetime import timedelta

from django.utils import timezone

from subscription.models import Voucher, Redemption
from subscription.utils import get_subscription


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

    num_days = 7

    subscription = get_subscription(user=user)

    until_date = get_until_date(subscription=subscription, num_days=num_days)

    voucher = {
        "code": code,
        "num_days": num_days,
        "until_date": until_date,
    }

    return voucher
