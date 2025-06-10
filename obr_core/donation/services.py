import logging
import pprint

from django.conf import settings
from django.core.cache import cache

import stripe
import stripe.error
from donation.models import Donation

logger = logging.getLogger(__name__)

stripe.api_key = settings.STRIPE_SECRET_KEY


class ServiceError(Exception): ...


def price_options_list():

    seconds_valid = 15 * 60
    cache_key = "stripe-prices"

    prices = cache.get(cache_key)

    if prices is None:
        prices = stripe.Price.list(
            limit=100,
            active=True,
            expand=[
                "data.currency_options",
            ],
        )
        cache.set(cache_key, prices, seconds_valid)

    options = []
    for price in prices.data:
        for currency, opts in price.currency_options.items():
            options.append(
                {
                    "price_id": price.id,
                    "lookup_key": price.lookup_key,
                    "amount": opts["unit_amount"] / 100,
                    "currency": currency.upper(),
                },
            )

    return options


def customer_get_for_user(*, user):

    customer = None

    if stripe_customer_id := user.stripe_customer_id:
        try:
            existing_customer = stripe.Customer.retrieve(
                stripe_customer_id,
            )
            customer = (
                existing_customer if not hasattr(existing_customer, "deleted") else None
            )
        except stripe.error.InvalidRequestError as e:
            logger.error(f"Error retrieving customer: {e}")

    if not customer:
        customer = stripe.Customer.create(
            email=user.email,
            name=user.full_name,
            metadata={
                "user_uid": user.uid,
            },
        )

        # NOTE: maybe we should not have a side effect here?
        user.stripe_customer_id = customer.id
        user.save(update_fields=["stripe_customer_id"])

    return customer


def payment_single_create_for_donation(
    *,
    donation,
    customer: stripe.Customer | None,
) -> stripe.PaymentIntent:
    payment_intent = None
    payment_intent_description = (
        f"Donation:  {donation.currency.upper()} {donation.amount:.2f}"
    )

    if donation.payment_intent_id:
        try:
            payment_intent = stripe.PaymentIntent.modify(
                donation.payment_intent_id,
                amount=int(round(donation.amount * 100)),
                currency=donation.currency,
                description=payment_intent_description,
            )
        except stripe.error.InvalidRequestError as e:
            # If the payment intent is not found or invalid, create a new one
            logger.error(f"Error modifying payment intent: {e}")
            payment_intent = None

    if not payment_intent:
        payment_intent = stripe.PaymentIntent.create(
            amount=int(round(donation.amount * 100)),
            currency=donation.currency,
            automatic_payment_methods={"enabled": True},
            customer=customer.id if customer else None,
            description=payment_intent_description,
            metadata={
                "obj_key": donation.ct_uid,
                "donation_uid": donation.uid,
            },
        )

    return payment_intent


def payment_recurring_create_for_donation(
    *,
    donation,
    customer: stripe.Customer,
) -> stripe.Subscription:

    try:
        subscription = stripe.Subscription.create(
            customer=customer.id,
            currency=donation.currency,
            items=[
                {
                    "price": donation.price_id,
                },
            ],
            metadata={
                "obj_key": donation.ct_uid,
                "donation_uid": donation.uid,
            },
            payment_behavior="default_incomplete",
            payment_settings={"save_default_payment_method": "on_subscription"},
            expand=[
                "latest_invoice.confirmation_secret",
                "latest_invoice.payment_intent",
            ],
        )
    except stripe.error.InvalidRequestError as e:
        logger.error(f"error creating subscription: {e}")
        raise ServiceError(str(e))

    return subscription


def payment_finalize_for_donation(
    *,
    donation: Donation,
) -> Donation:

    if donation.state != Donation.State.PENDING:
        logger.info(f"not in pending state: {donation}")
        return donation

    if donation.kind == Donation.Kind.SINGLE:

        payment_intent = stripe.PaymentIntent.retrieve(
            donation.payment_intent_id,
        )

        state = (
            Donation.State.SUCCEEDED
            if payment_intent.status == "succeeded"
            else Donation.State.FAILED
        )

        Donation.objects.filter(pk=donation.pk).update(
            state=state,
            payment_intent_data=payment_intent,
        )

    if donation.kind == Donation.Kind.RECURRING:

        payment_intent = stripe.PaymentIntent.retrieve(
            donation.payment_intent_id,
        )

        subscription = stripe.Subscription.retrieve(
            donation.subscription_id,
        )

        state = (
            Donation.State.ACTIVE if subscription.plan.active else Donation.State.FAILED
        )

        Donation.objects.filter(pk=donation.pk).update(
            state=state,
            payment_intent_data=payment_intent,
            subscription_data=subscription,
        )

    donation.refresh_from_db()

    return donation


def payment_update_from_event(
    *,
    event: stripe.Event,
) -> None:
    # NOTE: see donation.signals - where we "pre-filter" the events

    event_type = event.type
    event_object = event.data.object
    metadata = event_object.metadata
    obj_key = metadata.obj_key
    obj_ct, obj_uid = obj_key.split(":")

    pprint.pp(event_type)

    if event_type == "payment_intent.succeeded":
        donation = Donation.objects.get(uid=obj_uid)
        print("donation", donation, donation.state)
        if donation.state == Donation.State.PENDING:
            payment_finalize_for_donation(donation=donation)

    if event_type == "customer.subscription.updated":
        donation = Donation.objects.get(uid=obj_uid)
        print("update donation", donation, donation.state)
        subscription = event_object
        plan = subscription.plan
        pprint.pp(subscription)
        pprint.pp(plan)

        Donation.objects.filter(pk=donation.pk).update(
            amount=plan.amount / 100,
            currency=plan.currency.upper(),
            price_id=plan.id,
            subscription_data=subscription,
        )

    if event_type == "customer.subscription.deleted":
        donation = Donation.objects.get(uid=obj_uid)
        print("cancel donation", donation, donation.state)
        subscription = event_object
        plan = subscription.plan
        pprint.pp(subscription)
        pprint.pp(plan)

        Donation.objects.filter(pk=donation.pk).update(
            state=Donation.State.CANCELED,
            amount=plan.amount / 100,
            currency=plan.currency.upper(),
            price_id=plan.id,
            subscription_data=subscription,
        )


def donation_cancel_on_stripe(
    *,
    donation: Donation,
) -> None:
    try:
        stripe.Subscription.cancel(donation.subscription_id)
    except stripe.error.InvalidRequestError as e:
        logger.error(f"Error canceling subscription: {e}")
        raise ServiceError(str(e))
