import logging
from decimal import Decimal

from django.conf import settings
from django.urls import reverse

import stripe
from base.utils.signer import timestamp_signer
from base.utils.urls import get_absolute_url

logger = logging.getLogger(__name__)

PUBLISHABLE_KEY = getattr(settings, "STRIPE_PUBLISHABLE_KEY")
SECRET_KEY = getattr(settings, "STRIPE_SECRET_KEY")


def create_checkout_session(request, user, items, payment):
    stripe.api_key = SECRET_KEY

    email = user.email

    user_uid = str(user.uid)
    payment_uid = str(payment.uid)
    signed_payment_uid = timestamp_signer.sign(payment_uid)

    success_url = (
        get_absolute_url(
            request,
            reverse(
                "api:subscription:stripe:success",
                kwargs={
                    "signed_payment_uid": signed_payment_uid,
                },
            ),
        )
        + "?session_id={CHECKOUT_SESSION_ID}"
    )

    cancel_url = get_absolute_url(request, "/account/settings/")

    print(success_url)
    print(cancel_url)

    line_items = []
    for item in items:
        line_items.append(
            {
                "price_data": {
                    "currency": "CHF",
                    "product_data": {
                        "name": item["title"],
                        "metadata": {
                            "sku": item["title"],
                        },
                        # "images": [],
                    },
                    "unit_amount": int(item["price"] * Decimal(100)),
                    # "recurring": {
                    #     "interval": "month",
                    # },
                },
                "quantity": 1,
            }
        )

    # sc = stripe.Charge.create()

    metadata = {
        "user_uid": user_uid,
        "payment_uid": payment_uid,
        "email": email,
    }

    print(line_items)

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        mode="payment",
        client_reference_id=payment_uid,
        customer_email=email,
        line_items=line_items,
        payment_intent_data={
            "metadata": metadata,
            "receipt_email": email,
        },
        success_url=success_url,
        cancel_url=cancel_url,
    )

    print(session)

    return session


def get_checkout_session(request):
    stripe.api_key = SECRET_KEY
    session_id = request.GET.get("session_id", None)
    session = stripe.checkout.Session.retrieve(session_id)
    return session


def complete_checkout_session(session, payment):
    transaction_id = session.get("id")
    amount = session.get("amount_total", 0) * 0.01
    currency = session.get("currency")
    state = session.get("payment_status")

    if state == "paid" and not payment.is_paid:
        payment.set_state_paid(
            transaction_id=transaction_id,
            amount=amount,
            currency=currency,
        )
        payment.save()

    logger.info(
        "completed checkout",
        {
            "state": state,
            "transaction_id": transaction_id,
            "amount": amount,
            "currency": currency,
        },
    )
