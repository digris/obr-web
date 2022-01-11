from django.urls import reverse
from rest_flex_fields.serializers import FlexFieldsSerializerMixin
from rest_framework import serializers
from django_countries.serializer_fields import CountryField
from django_countries import countries
from social_django.models import UserSocialAuth

from account.models import User, Settings, Address
from subscription.models import Subscription


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(
        write_only=True,
    )


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8,
    )


class SettingsSerializer(
    serializers.ModelSerializer,
):
    class Meta:
        model = Settings
        fields = [
            "ct",
            "uid",
        ]


class AddressSerializer(
    serializers.ModelSerializer,
):
    country = CountryField(required=False, country_dict=True)

    country_options = serializers.SerializerMethodField(read_only=True, allow_null=True)

    class Meta:
        model = Address
        fields = [
            "ct",
            "uid",
            "line_1",
            "line_2",
            "postal_code",
            "city",
            "country",
            "country_options",
        ]

    @staticmethod
    def get_country_options(*args, **kwargs):
        for code, name in list(countries):
            yield {
                "code": code,
                "name": name,
            }

    # def get_country_options(self, obj):
    #     for code, name in list(countries):
    #         yield {
    #             "code": code,
    #             "name": name,
    #             "selected": obj.country == code,
    #         }


class SubscriptionSerializer(
    serializers.ModelSerializer,
):
    class Meta:
        model = Subscription
        fields = [
            "ct",
            "uid",
            "active_until",
            "is_active",
            "is_trial",
        ]


class UserSerializer(
    FlexFieldsSerializerMixin,
    serializers.ModelSerializer,
):
    class Meta:
        model = User
        fields = [
            "ct",
            "uid",
            "email",
            "date_joined",
            "first_name",
            "last_name",
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

    def get_can_disconnect(self, obj):
        return obj.allowed_to_disconnect(
            user=obj.user,
            backend_name=str(obj.provider),
            association_id=obj.id,
        )

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
