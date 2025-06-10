import logging

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from donation import services
from donation.models import Donation
from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger(__name__)


class DonationOptionsView(
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
            ref_name = "DonationOptionsView"

    @extend_schema(
        operation_id="donation_options",
        responses={status.HTTP_200_OK: OutputSerializer},
    )
    def get(self, request):

        options = services.price_options_list()

        serializer = self.OutputSerializer(
            options,
            many=True,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class DonationCreateView(
    APIView,
):

    class InputSerializer(serializers.Serializer):
        kind = serializers.ChoiceField(
            choices=Donation.Kind.choices,
        )
        amount = serializers.IntegerField(
            min_value=1,
            max_value=10000,
            required=True,
        )
        currency = serializers.CharField(
            max_length=3,
            default="CHF",
        )
        price_id = serializers.CharField(
            max_length=32,
            required=False,
        )

        def validate(self, attrs):
            kind = attrs.get("kind")
            price_id = attrs.get("price_id")

            if kind == Donation.Kind.RECURRING and not price_id:
                raise serializers.ValidationError(
                    {
                        "price_id": f"Price ID is required for kind: {kind}",
                    },
                )

            return attrs

    class OutputSerializer(serializers.Serializer):
        uid = serializers.CharField()
        client_secret = serializers.CharField(
            max_length=255,
            required=True,
        )

        class Meta:
            ref_name = "DonationCreateView"

    @extend_schema(
        operation_id="donation_create",
        responses={status.HTTP_200_OK: OutputSerializer},
    )
    def post(self, request):

        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        input_data = input_serializer.validated_data

        # check for existing pending donation / payment intent
        lookup = {
            "state": Donation.State.PENDING,
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

        donation, _ = Donation.objects.update_or_create(
            **lookup,
            defaults=input_data,
        )

        customer = (
            services.customer_get_for_user(user=request.user)
            if request.user.is_authenticated
            else None
        )

        if donation.kind == Donation.Kind.SINGLE:

            payment_intent = services.payment_single_create_for_donation(
                donation=donation,
                customer=customer,
            )

            Donation.objects.filter(pk=donation.pk).update(
                payment_intent_id=payment_intent.id,
                payment_intent_data=payment_intent,
            )

            client_secret = payment_intent.client_secret

        elif donation.kind == Donation.Kind.RECURRING:

            try:
                subscription = services.payment_recurring_create_for_donation(
                    donation=donation,
                    customer=customer,
                )
            except services.ServiceError as e:
                logger.error(f"Error creating payment intent: {e}")
                return Response(
                    {
                        "message": str(e),
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            client_secret = (
                subscription.latest_invoice.confirmation_secret.client_secret
            )

            # NOTE: not sure if this is a good idea... we use secret first part as id
            Donation.objects.filter(pk=donation.pk).update(
                payment_intent_id=client_secret.split("_secret_")[0],
                subscription_id=subscription.id,
                subscription_data=subscription,
            )

        else:
            # NOTE: this actually should not happe as, as the serializer validates this
            raise serializers.ValidationError(
                {
                    "kind": f"Unsupported kind: {input_data['kind']}",
                },
            )

        serializer = self.OutputSerializer(
            {
                "uid": donation.uid,
                "client_secret": client_secret,
            },
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class DonationFinalizeView(
    APIView,
):

    class OutputSerializer(serializers.Serializer):
        uid = serializers.CharField(max_length=8)
        kind = serializers.ChoiceField(
            choices=Donation.Kind.choices,
        )
        state = serializers.ChoiceField(
            choices=Donation.State.choices,
        )

        class Meta:
            ref_name = "DonationFinalizeView"

    @extend_schema(
        operation_id="donation_finalize",
        responses={status.HTTP_200_OK: OutputSerializer},
    )
    def post(self, request, payment_intent_id: str):

        donation = get_object_or_404(
            Donation,
            payment_intent_id=payment_intent_id,
        )

        donation = services.payment_finalize_for_donation(donation=donation)

        serializer = self.OutputSerializer(
            {
                "uid": donation.uid,
                "kind": donation.kind,
                "state": donation.state,
            },
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class DonationReturnView(
    APIView,
):

    @extend_schema(
        operation_id="donation_return",
        responses={status.HTTP_302_FOUND: None},
    )
    def get(self, request):
        next_url = request.GET.get("next", "/")
        payment_intent_id = request.GET.get("payment_intent")

        donation = get_object_or_404(
            Donation,
            payment_intent_id=payment_intent_id,
        )

        donation = services.payment_finalize_for_donation(donation=donation)

        if donation.state == Donation.State.FAILED:
            return HttpResponseRedirect(f"{next_url}#donate:failed")

        return HttpResponseRedirect(f"{next_url}#donate:success")
