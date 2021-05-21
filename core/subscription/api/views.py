# -*- coding: utf-8 -*-
import logging

from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions

from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.reverse import reverse

from subscription.models import Subscription

from subscription.utils import trial, plan
from subscription.api.serializers import serializers


logger = logging.getLogger(__name__)


class SubscriptionView(APIView):
    @staticmethod
    def get(request):
        user = request.user
        if user.is_authenticated and hasattr(user, "subscription"):
            subscription = request.user.subscription
            serializer = serializers.SubscriptionSerializer(
                subscription,
                context={
                    "request": request,
                },
            )
            response = Response(serializer.data)

        else:
            response = Response(status=status.HTTP_204_NO_CONTENT)

        return response


class SubscriptionTrialView(APIView):

    permission_classes = [
        permissions.IsAuthenticated,
    ]

    @staticmethod
    def get(request):
        user = request.user
        if hasattr(user, "subscription"):
            return Response(
                {
                    "message": "Already subscribed. No trial subscription possible.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        options = trial.get_options(user=request.user)
        data = {
            "message": "Get ccess to all content on site without restrictions.",
            "options": options,
        }

        return Response(data)

    @staticmethod
    def put(request):
        user = request.user
        if hasattr(user, "subscription"):
            return Response(
                {
                    "message": "Already subscribed. No trial subscription possible.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        trial.start_trial(user=user)

        data = {
            "location": reverse(
                "api:subscription:subscription",
                request=request,
            ),
        }

        return Response(data, status=status.HTTP_201_CREATED)


class SubscriptionPlanView(APIView):

    permission_classes = [
        permissions.IsAuthenticated,
    ]

    @staticmethod
    def get(request):
        options = plan.get_options(user=request.user)
        data = {
            "message": "Choose your plan.",
            "options": options,
        }

        return Response(data)


class PaymentView(APIView):

    permission_classes = [
        permissions.IsAuthenticated,
    ]

    @staticmethod
    def get(request):
        data = [
            {
                "name": "Credit Card",
                "key": "stripe",
                "endpoint": reverse(f"api:subscription:stripe:endpoint"),
            },
        ]

        return Response(data)

    # @staticmethod
    # def post(request):
    #     user = request.user
    #     provider = request.data.get("provider")
    #
    #     return Response()
