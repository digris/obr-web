# -*- coding: utf-8 -*-
import logging

from django import dispatch

from account.signals import user_registered

logger = logging.getLogger(__name__)

payment_completed = dispatch.Signal(
    providing_args=[
        "payment",
    ]
)


@dispatch.receiver(payment_completed)
def handle_payment_completed(sender, payment, *args, **kwargs):

    from subscription.utils.plan import extend_subscription

    logger.info(f"Payment paid signal received: {payment}")

    try:
        num_days = payment.extra_data["plan"]["num_days"]
        extend_subscription(user=payment.user, num_days=num_days)
    except KeyError:
        logger.warning("unable to get extra_data / num_days", payment.extra_data)
        return


@dispatch.receiver(user_registered)
def handle_user_registered(sender, user, *args, **kwargs):
    from subscription.utils import trial

    print("subscription - handle_user_registered", user)
    trial.start_trial(user=user)
