import logging
import pprint

from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponseRedirect

import stripe
import stripe.error
from common.api.serializers import inline_serializer
from donation.models import RecurringDonation, SingleDonation
from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger(__name__)

stripe.api_key = settings.STRIPE_SECRET_KEY


class SingleDonationCreateView(
    APIView,
):

    class InputSerializer(serializers.Serializer):
        amount = serializers.IntegerField(
            min_value=1,
            max_value=10000,
            required=True,
        )
        currency = serializers.CharField(
            max_length=3,
            default="eur",
        )

    class OutputSerializer(serializers.Serializer):
        uid = serializers.CharField()
        amount = serializers.IntegerField(
            min_value=1,
            max_value=10000,
        )
        payment_id = serializers.CharField(
            max_length=255,
            required=True,
        )
        client_secret = serializers.CharField(
            max_length=255,
            required=True,
        )

        class Meta:
            ref_name = "SingleDonationCreateView"

    @extend_schema(
        operation_id="donation_single_create",
        responses={status.HTTP_200_OK: OutputSerializer},
    )
    def post(self, request):

        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        input_data = input_serializer.validated_data

        # check for existing pending donation / payment intent
        lookup = {
            "state": SingleDonation.State.PENDING,
        }
        if request.user.is_authenticated:
            lookup.update(
                {
                    "user": request.user,
                },
            )
        else:
            lookup.update(
                {
                    "user_identity": request.user_identity,
                },
            )

        try:
            donation = SingleDonation.objects.get(**lookup)
            SingleDonation.objects.filter(pk=donation.pk).update(
                amount=input_data["amount"],
                currency=input_data["currency"],
            )
        except SingleDonation.DoesNotExist:
            donation = SingleDonation.objects.create(
                amount=input_data["amount"],
                currency=input_data["currency"],
                **lookup,
            )

        ###############################################################
        # create or retrieve the customer
        ###############################################################
        customer = None

        if request.user.is_authenticated:
            if stripe_customer_id := request.user.stripe_customer_id:
                try:
                    existing_customer = stripe.Customer.retrieve(
                        stripe_customer_id,
                    )
                    customer = (
                        existing_customer
                        if not hasattr(existing_customer, "deleted")
                        else None
                    )
                except stripe.error.InvalidRequestError as e:
                    logger.error(f"Error retrieving customer: {e}")
                    customer = None

            if not customer:
                customer = stripe.Customer.create(
                    email=request.user.email,
                    name=request.user.full_name,
                    metadata={
                        "user_uid": request.user.uid,
                    },
                )
                request.user.stripe_customer_id = customer.id
                request.user.save(update_fields=["stripe_customer_id"])

        ###############################################################
        # create or modify the payment intent
        ###############################################################
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
                receipt_email=(
                    request.user.email if request.user.is_authenticated else None
                ),
                metadata={
                    "donation_uid": donation.uid,
                },
            )

        SingleDonation.objects.filter(pk=donation.pk).update(
            payment_intent_id=payment_intent.id,
        )

        serializer = self.OutputSerializer(
            {
                "uid": donation.uid,
                "amount": payment_intent.get("amount"),
                "payment_id": payment_intent.get("id"),
                "client_secret": payment_intent.get("client_secret"),
            },
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class SingleDonationFinalizeView(
    APIView,
):

    class OutputSerializer(serializers.Serializer):
        uid = serializers.CharField(max_length=8)

        class Meta:
            ref_name = "SingleDonationFinalizeView"

    @extend_schema(
        operation_id="donation_single_finalize",
        responses={status.HTTP_200_OK: OutputSerializer},
    )
    def post(self, request, payment_intent_id: str):

        donation = SingleDonation.objects.get(
            payment_intent_id=payment_intent_id,
        )

        payment_intent = stripe.PaymentIntent.retrieve(
            donation.payment_intent_id,
        )

        pprint.pprint(payment_intent)

        state = (
            SingleDonation.State.SUCCEEDED
            if payment_intent.status == "succeeded"
            else SingleDonation.State.FAILED
        )

        SingleDonation.objects.filter(pk=donation.pk).update(
            state=state,
            extra_data=payment_intent,
        )

        serializer = self.OutputSerializer(
            {
                "uid": donation.uid,
            },
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class SingleDonationReturnView(
    APIView,
):

    @extend_schema(
        operation_id="donation_single_return",
        responses={status.HTTP_302_FOUND: None},
    )
    def get(self, request):
        next_url = request.GET.get("next", "/")
        payment_intent_id = request.GET.get("payment_intent")

        donation = SingleDonation.objects.get(
            payment_intent_id=payment_intent_id,
        )

        payment_intent = stripe.PaymentIntent.retrieve(
            donation.payment_intent_id,
        )

        pprint.pprint(payment_intent)

        state = (
            SingleDonation.State.SUCCEEDED
            if payment_intent.status == "succeeded"
            else SingleDonation.State.FAILED
        )

        SingleDonation.objects.filter(pk=donation.pk).update(
            state=state,
            extra_data=payment_intent,
        )

        return HttpResponseRedirect(f"{next_url}#donate:success")


class RecurringDonationOptionsView(
    APIView,
):

    class OutputSerializer(serializers.Serializer):
        price_id = serializers.CharField(
            max_length=32,
            required=True,
        )
        lookup_key = serializers.CharField(
            max_length=255,
            required=True,
        )
        amount = serializers.IntegerField(
            min_value=1,
            max_value=10000,
        )
        currency = serializers.CharField(
            max_length=3,
            required=True,
        )

        class Meta:
            ref_name = "RecurringDonationOptionsView"

    @extend_schema(
        operation_id="donation_recurring_create",
        responses={status.HTTP_200_OK: OutputSerializer},
    )
    def get(self, request):

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
            pprint.pp(price)
            for currency, opts in price.currency_options.items():
                options.append(
                    {
                        "price_id": price.id,
                        "lookup_key": price.lookup_key,
                        "amount": opts["unit_amount"] / 100,
                        "currency": currency.upper(),
                    },
                )

        serializer = self.OutputSerializer(
            options,
            many=True,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class RecurringDonationCreateView(
    APIView,
):

    class InputSerializer(serializers.Serializer):
        price_id = serializers.CharField(
            max_length=32,
            required=True,
        )
        amount = serializers.IntegerField(
            min_value=1,
            max_value=10000,
            required=True,
        )
        currency = serializers.CharField(
            max_length=3,
            default="eur",
        )

    class OutputSerializer(serializers.Serializer):
        amount = serializers.IntegerField(
            min_value=1,
            max_value=10000,
        )
        subscription_id = serializers.CharField(
            max_length=255,
            required=True,
        )
        client_secret = serializers.CharField(
            max_length=255,
            required=True,
        )

        class Meta:
            ref_name = "SingleDonationCreateView"

    @extend_schema(
        operation_id="donation_recurring_create",
        responses={status.HTTP_200_OK: OutputSerializer},
    )
    def post(self, request):

        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        input_data = input_serializer.validated_data

        print("input_data", input_data)

        donation, _ = RecurringDonation.objects.update_or_create(
            user=request.user,
            defaults=input_data,
        )

        print("donation", donation)

        ###############################################################
        # create or retrieve the customer
        ###############################################################
        customer = None

        if stripe_customer_id := request.user.stripe_customer_id:
            try:
                existing_customer = stripe.Customer.retrieve(
                    stripe_customer_id,
                )
                customer = (
                    existing_customer
                    if not hasattr(existing_customer, "deleted")
                    else None
                )
            except stripe.error.InvalidRequestError as e:
                logger.error(f"Error retrieving customer: {e}")
                customer = None

        if not customer:
            customer = stripe.Customer.create(
                email=request.user.email,
                name=request.user.full_name,
                metadata={
                    "user_uid": request.user.uid,
                },
            )
            request.user.stripe_customer_id = customer.id
            request.user.save(update_fields=["stripe_customer_id"])

        pprint.pprint(customer)

        try:
            subscription = stripe.Subscription.create(
                customer=customer.id,
                currency=donation.currency,
                items=[
                    {
                        "price": input_data["price_id"],
                    },
                ],
                payment_behavior="default_incomplete",
                payment_settings={"save_default_payment_method": "on_subscription"},
                expand=["latest_invoice.confirmation_secret"],
            )
        except stripe.error.InvalidRequestError as e:
            logger.error(f"Error creating subscription: {e}")
            return Response(
                {
                    "message": str(e),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        print("*" * 72)

        print("subscription", subscription)

        RecurringDonation.objects.filter(pk=donation.pk).update(
            payment_intent_id=subscription.latest_invoice.payment_intent,
        )

        serializer = self.OutputSerializer(
            {
                "amount": 0,
                "subscription_id": subscription.id,
                "client_secret": subscription.latest_invoice.confirmation_secret.client_secret,
            },
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class RecurringDonationFinalizeView(
    APIView,
):

    class OutputSerializer(serializers.Serializer):
        uid = serializers.CharField(max_length=8)
        invoice = inline_serializer(
            fields={
                "hosted_invoice_url": serializers.URLField(),
                "pdf_invoice_url": serializers.URLField(),
            },
        )

        class Meta:
            ref_name = "RecurringDonationFinalizeView"

    @extend_schema(
        operation_id="donation_recurring_finalize",
        responses={status.HTTP_200_OK: OutputSerializer},
    )
    def post(self, request, payment_intent_id: str):

        donation = RecurringDonation.objects.get(
            payment_intent_id=payment_intent_id,
        )

        payment_intent = stripe.PaymentIntent.retrieve(
            donation.payment_intent_id,
            expand=[
                "invoice",
                "invoice.subscription",
            ],
        )
        invoice = payment_intent.invoice
        subscription = invoice.subscription

        print("*" * 72)
        pprint.pp(invoice)
        print("-" * 72)
        pprint.pp(subscription)
        print("*" * 72)

        state = (
            RecurringDonation.State.ACTIVE
            if subscription.plan.active
            else RecurringDonation.State.FAILED
        )

        RecurringDonation.objects.filter(pk=donation.pk).update(
            state=state,
            subscription_id=subscription.id,
            extra_data=subscription,
        )

        serializer = self.OutputSerializer(
            {
                "uid": donation.uid,
                "invoice": {
                    "hosted_invoice_url": invoice.hosted_invoice_url,
                    "pdf_invoice_url": invoice.invoice_pdf,
                },
            },
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class RecurringDonationReturnView(
    APIView,
):

    @extend_schema(
        operation_id="donation_recurring_return",
        responses={status.HTTP_302_FOUND: None},
    )
    def get(self, request):
        next_url = request.GET.get("next", "/")
        payment_intent_id = request.GET.get("payment_intent")

        donation = RecurringDonation.objects.get(
            payment_intent_id=payment_intent_id,
        )

        payment_intent = stripe.PaymentIntent.retrieve(
            donation.payment_intent_id,
            expand=[
                "invoice",
                "invoice.subscription",
            ],
        )
        invoice = payment_intent.invoice
        subscription = invoice.subscription

        state = (
            RecurringDonation.State.ACTIVE
            if subscription.plan.active
            else RecurringDonation.State.FAILED
        )

        RecurringDonation.objects.filter(pk=donation.pk).update(
            state=state,
            subscription_id=subscription.id,
            extra_data=subscription,
        )

        return HttpResponseRedirect(f"{next_url}#donate:success")
