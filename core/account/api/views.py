# -*- coding: utf-8 -*-
import logging

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema

from account import email_login, token_login
from account.cdn_credentials.utils import (
    set_credentials,
    remove_credentials,
)
from account.models import User
from account.utils import social_backends
from . import serializers

logger = logging.getLogger(__name__)


class UserView(APIView):
    @staticmethod
    def get(request):
        if request.user.is_authenticated:
            serializer = serializers.UserSerializer(
                request.user,
                context={
                    "request": request,
                },
            )
            response = Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )

            if request.user.has_active_subscription:
                response = set_credentials(response)
            else:
                response = remove_credentials(response)
        else:
            response = Response()
            response = remove_credentials(response)
        return response


@method_decorator(csrf_exempt, name="dispatch")
class LoginView(APIView):
    @staticmethod
    def post(request):
        user = authenticate(**request.data)
        if user is not None:
            login(request, user)
            serializer = serializers.UserSerializer(
                user,
                context={
                    "request": request,
                },
            )
            response = Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )

            if request.user.has_active_subscription:
                response = set_credentials(response)
            else:
                response = remove_credentials(response)
        else:
            response = Response(
                {
                    "message": "The email or password you entered is incorrect.",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
        return response


@method_decorator(csrf_exempt, name="dispatch")
class SendEmailLoginView(APIView):

    throttle_scope = "account.login_email"

    @staticmethod
    def get(request):
        email = request.GET.get("email", None)

        if not email:
            return Response(
                {
                    "message": 'query parameter "email" missing.',
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(email=email.replace(' ', '+'))
            return Response(
                {
                    "ct": user.ct,
                    "uid": user.uid,
                    "has_usable_password": user.has_usable_password(),
                },
                status=status.HTTP_200_OK,
            )
        except User.DoesNotExist:
            return Response(
                None,
                status=status.HTTP_204_NO_CONTENT,
            )

    @staticmethod
    def post(request):
        email = request.data.get("email")
        try:
            email_login.send_login_email(email=email)
        except email_login.SendLoginEmailException as e:
            return Response(
                {
                    "message": f"{e}",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = {
            "email": email,
            "message": f"Sent login information to {email}",
        }
        response = Response(
            data,
            status=status.HTTP_200_OK,
        )

        return response


@method_decorator(csrf_exempt, name="dispatch")
class TokenLoginView(APIView):
    @staticmethod
    def post(request):
        email = request.data.get("email")
        token = request.data.get("token")

        try:
            email = token_login.claim_token(
                email=email,
                token=token,
            )
        except token_login.TokenValidationException as e:
            return Response(
                {
                    "message": f"{e}",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_created = False
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User(email=email)
            user.set_unusable_password()
            user.save()
            user_created = True

        login(
            request,
            user,
            backend=settings.AUTHENTICATION_BACKENDS[-1],
        )

        serializer = serializers.UserSerializer(
            user,
            context={
                "request": request,
            },
        )

        response = Response(
            serializer.data,
            status=status.HTTP_201_CREATED if user_created else status.HTTP_200_OK,
        )

        if user.has_active_subscription:
            response = set_credentials(response)
        else:
            response = remove_credentials(response)

        return response


@method_decorator(csrf_exempt, name="dispatch")
class SignedEmailLoginView(APIView):
    @staticmethod
    def post(request):
        signed_email = request.data.get("signed_email")

        try:
            email = email_login.validate_signed_email(
                signed_email=signed_email,
                max_age=60 * 60,
            )
        except email_login.SignedEmailValidationException as e:
            return Response(
                {
                    "message": f"{e}",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # user, user_created = User.objects.get_or_create(email=email)
        user_created = False
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User(email=email)
            user.set_unusable_password()
            user.save()
            user_created = True

        login(
            request,
            user,
            backend=settings.AUTHENTICATION_BACKENDS[-1],
        )

        serializer = serializers.UserSerializer(
            user,
            context={
                "request": request,
            },
        )

        response = Response(
            serializer.data,
            status=status.HTTP_201_CREATED if user_created else status.HTTP_200_OK,
        )

        if user.has_active_subscription:
            response = set_credentials(response)
        else:
            response = remove_credentials(response)

        return response


@method_decorator(csrf_exempt, name="dispatch")
class LogoutView(APIView):
    @staticmethod
    # pylint: disable=unused-argument
    def post(request, *args, **kwargs):
        logout(request)
        response = Response(
            None,
            status=status.HTTP_205_RESET_CONTENT,
        )
        response = remove_credentials(response)
        return response


# class CredentialsView(APIView):
#     @staticmethod
#     # pylint: disable=unused-argument
#     def get(request, *args, **kwargs):
#         # logger.debug("headers", request.headers)
#         if request.user.is_authenticated:
#             seconds_valid = 60 * 60
#             logger.info(
#                 "refresh credentials",
#                 {
#                     "user": str(request.user),
#                     "seconds_valid": seconds_valid,
#                 },
#             )
#             response = Response(
#                 {
#                     "seconds_valid": seconds_valid,
#                 },
#                 status=status.HTTP_200_OK,
#             )
#             response = set_credentials(response, seconds_valid=seconds_valid)
#         else:
#             response = Response(
#                 None,
#                 status=status.HTTP_204_NO_CONTENT,
#             )
#             response = remove_credentials(response)
#         return response


class SocialBackendListView(APIView):
    """
    returns all connected and disconnected social backends.
    (based on requests current user)
    """

    @staticmethod
    @extend_schema(
        parameters=[
            serializers.SocialBackendsSerializer,
        ],
    )
    # pylint: disable=unused-argument
    def get(request, *args, **kwargs):
        # logger.debug("headers", request.headers)
        backends = social_backends.get_backends_for_user(request.user)

        serializer = serializers.SocialBackendsSerializer(
            backends,
            context={
                "request": request,
            },
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


class SocialBackendDetailView(APIView):
    """
    single backend association.
    (based on requests current user)
    this resource is only used to "disconnect" from a backend.
    """

    @staticmethod
    # pylint: disable=unused-argument
    def delete(request, *args, **kwargs):
        provider = kwargs.get("provider")
        uid = kwargs.get("uid")

        social_backends.disconnect_backend_for_user(
            request.user,
            provider=provider,
            uid=uid,
        )

        return Response(
            None,
            status=status.HTTP_204_NO_CONTENT,
        )
