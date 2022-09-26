from django.urls import reverse
from drf_spectacular.utils import extend_schema_field, OpenApiTypes
from rest_flex_fields.serializers import FlexFieldsSerializerMixin
from rest_framework import serializers
from social_django.models import UserSocialAuth

from api_extra.serializers import CTUIDModelSerializer
from account.models import User, Settings, Address
from subscription.models import Subscription


class ErrorMessageSerializer(
    serializers.Serializer,
):
    message = serializers.CharField(
        read_only=True,
    )


class LoginSerializer(
    serializers.Serializer,
):
    email = serializers.EmailField(
        write_only=True,
    )
    password = serializers.CharField(
        write_only=True,
    )


class SendEmailLoginLookupSerializer(
    serializers.Serializer,
):
    email = serializers.EmailField(
        write_only=True,
    )
    ct = serializers.CharField(
        read_only=True,
    )
    uid = serializers.CharField(
        read_only=True,
    )
    has_usable_password = serializers.BooleanField(
        read_only=True,
    )


class SendEmailLoginSerializer(
    serializers.Serializer,
):
    email = serializers.EmailField()
    message = serializers.CharField(
        read_only=True,
    )


class TokenLoginSerializer(
    serializers.Serializer,
):
    email = serializers.EmailField(
        write_only=True,
    )
    token = serializers.CharField(write_only=True, help_text="Login token e.g. ABC-DEF")


class SignedEmailLoginSerializer(
    serializers.Serializer,
):
    signed_email = serializers.CharField(
        write_only=True,
    )


class EmailUpdateSerializer(
    serializers.Serializer,
):
    email = serializers.EmailField(
        write_only=True,
    )


class PasswordUpdateSerializer(
    serializers.Serializer,
):
    password = serializers.CharField(
        write_only=True,
        min_length=8,
    )


class SettingsSerializer(
    CTUIDModelSerializer,
    serializers.ModelSerializer,
):
    class Meta(CTUIDModelSerializer.Meta):
        model = Settings
        fields = CTUIDModelSerializer.Meta.fields


class AddressSerializer(
    CTUIDModelSerializer,
    serializers.ModelSerializer,
):
    country = serializers.CharField(
        default="",
    )

    class Meta(CTUIDModelSerializer.Meta):
        model = Address
        fields = CTUIDModelSerializer.Meta.fields + [
            "line_1",
            "line_2",
            "postal_code",
            "city",
            "country",
        ]


class SubscriptionSerializer(
    CTUIDModelSerializer,
    serializers.ModelSerializer,
):
    class Meta(CTUIDModelSerializer.Meta):
        model = Subscription
        fields = CTUIDModelSerializer.Meta.fields + [
            "active_until",
            "is_active",
            "is_trial",
        ]


class UserSerializer(
    CTUIDModelSerializer,
    FlexFieldsSerializerMixin,
    serializers.ModelSerializer,
):
    email = serializers.EmailField(
        read_only=True,
    )
    date_joined = serializers.DateTimeField(
        read_only=True,
    )
    is_staff = serializers.BooleanField(
        read_only=True,
    )
    is_admin = serializers.BooleanField(
        source="is_superuser",
        read_only=True,
    )

    class Meta(CTUIDModelSerializer.Meta):
        model = User
        fields = CTUIDModelSerializer.Meta.fields + [
            "email",
            "date_joined",
            "first_name",
            "last_name",
            "is_staff",
            "is_admin",
        ]
        expandable_fields = {
            "settings": SettingsSerializer,
            "address": AddressSerializer,
            "subscription": SubscriptionSerializer,
        }


class SocialBackendSerializer(
    serializers.Serializer,
):
    def to_representation(self, instance):
        return {
            "provider": instance,
            "connect_url": reverse(
                "social:begin",
                kwargs={
                    "backend": str(instance),
                },
            ),
        }


class ConnectedSocialBackendSerializer(
    serializers.ModelSerializer,
):
    can_disconnect = serializers.SerializerMethodField()
    disconnect_url = serializers.SerializerMethodField()

    class Meta:
        model = UserSocialAuth
        fields = [
            "provider",
            "uid",
            "can_disconnect",
            "disconnect_url",
        ]

    @extend_schema_field(OpenApiTypes.BOOL)
    def get_can_disconnect(self, obj):
        return obj.allowed_to_disconnect(
            user=obj.user,
            backend_name=str(obj.provider),
            association_id=obj.id,
        )

    @extend_schema_field(OpenApiTypes.URI)
    def get_disconnect_url(self, obj):
        return reverse(
            "social:disconnect_individual",
            kwargs={
                "backend": str(obj.provider),
                "association_id": obj.id,
            },
            # args=[str(obj.provider)],
        )


class SocialBackendsSerializer(
    serializers.Serializer,
):
    connected = ConnectedSocialBackendSerializer(
        many=True,
        read_only=True,
    )
    disconnected = SocialBackendSerializer(
        many=True,
        read_only=True,
    )
    all = SocialBackendSerializer(
        many=True,
        read_only=True,
    )
    auth = SocialBackendSerializer(
        many=True,
        read_only=True,
    )
    sync = SocialBackendSerializer(
        many=True,
        read_only=True,
    )


class SocialBackendDisconnectSerializer(
    serializers.Serializer,
):
    provider = serializers.CharField(
        read_only=True,
    )
    uid = serializers.CharField(
        read_only=True,
    )
