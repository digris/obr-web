import re
from datetime import timedelta

from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from subscription.models import Redemption, Voucher
from subscription.utils import extend_subscription, get_subscription


class VoucherValidationError(Exception):
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
        raise VoucherValidationError(_("Malformed voucher-code"))

    qs = Voucher.objects.filter(code=code)

    if not qs.exists():
        raise VoucherValidationError(_("Voucher-code does not exist"))

    voucher = qs.first()

    if (
        user.is_authenticated
        and Redemption.objects.filter(voucher=voucher, user=user).exists()
    ):
        raise VoucherValidationError(_("You did already use this voucher-code"))

    # check if voucher is in inheritance tree
    if (
        user.is_authenticated
        and voucher.ancestors(include_self=True).filter(user=user).count()
    ):
        raise VoucherValidationError(
            _("You cannot use your own vouchers, or vouchers from people you invited."),
        )

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

    if voucher.inherit:
        Voucher.objects.create(
            parent=voucher,
            user=user,
            num_days=voucher.num_days,
            valid_until=voucher.valid_until,
            max_num_use=voucher.max_num_use,
            inherit=voucher.inherit,
        )

    return True
