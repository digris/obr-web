import logging

from django import dispatch

from account.signals import user_registered

logger = logging.getLogger(__name__)

payment_completed = dispatch.Signal()


@dispatch.receiver(payment_completed)
# pylint: disable=unused-argument
def handle_payment_completed(sender, payment, *args, **kwargs):
    # pylint: disable=import-outside-toplevel
    from subscription.utils import extend_subscription

    logger.info(f"Payment paid signal received: {payment}")

    try:
        num_days = payment.extra_data["plan"]["num_days"]
        extend_subscription(user=payment.user, num_days=num_days)
    except KeyError:
        logger.warning("unable to get extra_data / num_days", payment.extra_data)
        return


@dispatch.receiver(user_registered)
# pylint: disable=unused-argument
def handle_user_registered(sender, user, *args, **kwargs):
    # pylint: disable=import-outside-toplevel
    from subscription.utils import trial

    print("subscription - handle_user_registered", user)
    trial.start_trial(user=user)
