import logging

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from account import email_login, token_login
from account.cdn_credentials.utils import (
    set_credentials,
    remove_credentials,
)
from account.models import User, Address
from account.utils import social_backends
from . import serializers

logger = logging.getLogger(__name__)


class UserView(APIView):
    @staticmethod
    @extend_schema(
        responses={
            200: serializers.UserSerializer,
            204: None,
        },
        operation_id="user",
        description="Get current user",
    )
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
            response = Response(
                # NOTE: check for implications - was 200 with empty body before
                status=status.HTTP_204_NO_CONTENT,
            )
            response = remove_credentials(response)
        return response

    @staticmethod
    @extend_schema(
        request=serializers.UserSerializer,
        responses={
            200: serializers.UserSerializer,
        },
        operation_id="user_partial_update",
    )
    # pylint: disable=unused-argument
    def patch(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(
                {
                    "message": _("Not authorized"),
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        serializer = serializers.UserSerializer(
            request.user,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(
            raise_exception=True,
        )
        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


@method_decorator(
    csrf_exempt,
    name="dispatch",
)
class LoginView(APIView):
    @staticmethod
    @extend_schema(
        request=serializers.LoginSerializer,
        responses={
            200: serializers.UserSerializer,
        },
        methods=["POST"],
        operation_id="login",
        auth=[],
        description="Login user by email & password",
    )
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
                    "message": _("The email or password you entered is incorrect."),
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
        return response


@method_decorator(
    csrf_exempt,
    name="dispatch",
)
class SendEmailLoginView(APIView):

    throttle_scope = "account.login_email"

    @staticmethod
    @extend_schema(
        parameters=[
            serializers.SendEmailLoginLookupSerializer,
        ],
        request=None,
        responses={
            200: serializers.SendEmailLoginLookupSerializer,
            204: None,
        },
        operation_id="send_email_login_lookup",
        auth=[],
        description="Lookup if provided email can login by token",
    )
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
            user = User.objects.get(email=email.replace(" ", "+"))
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
    @extend_schema(
        methods=["POST"],
        request=serializers.SendEmailLoginSerializer,
        responses={
            200: serializers.SendEmailLoginSerializer,
        },
        operation_id="send_email_login",
        auth=[],
        description="Send email with login token to given address",
    )
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


@method_decorator(
    csrf_exempt,
    name="dispatch",
)
class TokenLoginView(APIView):
    @staticmethod
    @extend_schema(
        methods=["POST"],
        request=serializers.TokenLoginSerializer,
        responses={
            200: serializers.UserSerializer,
            201: serializers.UserSerializer,
        },
        operation_id="token_login",
        auth=[],
        description="Login user by email & token [ABC-DEF]",
    )
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


@method_decorator(
    csrf_exempt,
    name="dispatch",
)
class SignedEmailLoginView(APIView):
    @staticmethod
    @extend_schema(
        methods=["POST"],
        parameters=[
            serializers.SignedEmailLoginSerializer,
        ],
        request=None,
        responses={
            200: serializers.UserSerializer,
            201: serializers.UserSerializer,
        },
        operation_id="signed_email_login",
        auth=[],
        description="Login user by signed email",
    )
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


@method_decorator(
    csrf_exempt,
    name="dispatch",
)
class LogoutView(APIView):
    @staticmethod
    @extend_schema(
        methods=["POST"],
        request=None,
        responses={
            205: None,
        },
        operation_id="logout",
        description="Destroy user's session",
    )
    # pylint: disable=unused-argument
    def post(request, *args, **kwargs):
        logout(request)
        response = Response(
            None,
            status=status.HTTP_205_RESET_CONTENT,
        )
        response = remove_credentials(response)
        return response


class EmailUpdateView(APIView):
    @staticmethod
    @extend_schema(
        request=serializers.EmailUpdateSerializer,
        responses={
            204: None,
        },
        methods=["POST"],
        operation_id="user_update_email",
        description="Update or set email address",
    )
    # pylint: disable=unused-argument
    def post(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(
                {
                    "message": _("Not authorized"),
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        serializer = serializers.EmailUpdateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {
                    "message": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        email = serializer.validated_data.get("email")
        request.user.email = email
        request.user.save()

        response = Response(
            None,
            status=status.HTTP_204_NO_CONTENT,
        )
        return response


class PasswordUpdateView(APIView):
    @staticmethod
    @extend_schema(
        request=serializers.PasswordUpdateSerializer,
        responses={
            204: None,
        },
        methods=["POST"],
        operation_id="user_update_password",
        description="Update or set password",
    )
    # pylint: disable=unused-argument
    def post(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(
                {
                    "message": _("Not authorized"),
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        serializer = serializers.PasswordUpdateSerializer(
            data=request.data,
        )

        if not serializer.is_valid():
            return Response(
                {
                    "message": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        password = serializer.validated_data.get("password")
        request.user.set_password(password)
        request.user.save()

        login(
            request,
            request.user,
            backend=settings.AUTHENTICATION_BACKENDS[-1],
        )

        response = Response(
            None,
            status=status.HTTP_204_NO_CONTENT,
        )
        return response


class AddressUpdateView(APIView):

    serializer_class = serializers.AddressSerializer

    @staticmethod
    @extend_schema(
        request=serializers.AddressSerializer,
        responses={
            204: serializers.AddressSerializer,
        },
        methods=["PATCH"],
        operation_id="user_update_address",
    )
    # pylint: disable=unused-argument
    def patch(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(
                {
                    "message": _("Not authorized"),
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            address = request.user.address
        except Address.DoesNotExist:
            # TODO: implement actual geoip based country
            address = Address(
                user=request.user,
                country="CH",
            )
            address.save()

        serializer = serializers.AddressSerializer(
            address,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(
            raise_exception=True,
        )
        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class SocialBackendListView(APIView):
    """
    returns all connected and disconnected social backends.
    (based on requests current user)
    """

    @staticmethod
    @extend_schema(
        responses={
            200: serializers.SocialBackendsSerializer,
        },
        operation_id="social_backends",
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

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class SocialBackendDetailView(APIView):
    """
    single backend association.
    (based on requests current user)
    this resource is only used to "disconnect" from a backend.
    """

    @staticmethod
    @extend_schema(
        parameters=[
            serializers.SocialBackendDisconnectSerializer,
        ],
        methods=["DELETE"],
        responses={
            204: None,
        },
        operation_id="social_backend_disconnect",
    )
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
