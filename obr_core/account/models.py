from datetime import timedelta

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone

from account import signals as account_signals
from account import token_login
from account.cdn_credentials.policy import get_cdn_policy
from account.jwt_token.tokens import SlidingToken
from account.settings import LOGIN_TOKEN_MAX_AGE
from account.sync.user import sync_user
from common.models.mixins import CTUIDModelMixin
from django_countries.fields import CountryField
from sync.models.mixins import SyncModelMixin


class MigrationSource(models.TextChoices):
    EMPTY = "", "none"
    OBR = "obr", "OBR - radio"
    OBP = "obp", "OBP - platform"


class Gender(models.IntegerChoices):
    UNDEFINED = 0, "undefined"
    FEMALE = 1, "female"
    MALE = 2, "male"
    OTHER = 3, "other"


class GenderStr(models.TextChoices):
    UNDEFINED = "", "undefined"
    FEMALE = "female", "female"
    MALE = "male", "male"
    OTHER = "other", "other"


class NewsProvider(models.TextChoices):
    DISABLED = "", "none"
    SRF = "srf", "SRF"
    BBC = "bbc", "BBC"
    DLF = "dlf", "DLF"
    RFI = "rfi", "RFI"


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)


class User(
    CTUIDModelMixin,
    SyncModelMixin,
    AbstractBaseUser,
    PermissionsMixin,
):
    email = models.EmailField(
        "Email address",
        unique=True,
        db_index=True,
    )
    phone = models.CharField(
        max_length=64,
        blank=True,
        default="",
        db_index=True,
    )
    gender = models.CharField(
        max_length=16,
        choices=GenderStr.choices,
        default=GenderStr.UNDEFINED,
        blank=True,
    )
    first_name = models.CharField(
        max_length=64,
        default="",
        blank=True,
    )
    last_name = models.CharField(
        max_length=64,
        default="",
        blank=True,
    )
    country = CountryField(
        blank=True,
        default="",
    )
    year_of_birth = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1900), MaxValueValidator(2022)],
    )
    # NOTE: definitely not the best place..
    favorite_venue = models.CharField(
        max_length=64,
        default="",
        blank=True,
    )
    is_staff = models.BooleanField(
        default=False,
    )
    is_active = models.BooleanField(
        default=True,
    )
    date_joined = models.DateTimeField(
        default=timezone.now,
    )
    obp_id = models.PositiveIntegerField(
        verbose_name="open broadcast - platform ID",
        null=True,
        blank=True,
        db_index=True,
    )
    migration_source = models.CharField(
        max_length=64,
        choices=MigrationSource.choices,
        default=MigrationSource.EMPTY,
        blank=True,
        db_index=True,
    )

    # NOTE: maybe we should store this in a separate model?
    stripe_customer_id = models.CharField(
        max_length=64,
        default="",
        blank=True,
        db_index=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def sync_data(self, *args, **kwargs):
        return sync_user(self, *args, **kwargs)

    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        if self.first_name:
            return self.first_name
        return self.email

    @property
    def has_active_subscription(self):
        return (
            hasattr(self, "subscription")
            and self.subscription.is_active
            and not self.subscription.is_blocked
        )

    @property
    def access_token(self):
        timedelta(minutes=60 * 12)
        timedelta(days=28)
        return str(SlidingToken.for_user(self))

    @property
    def cdn_policy(self):
        if self.has_active_subscription:
            return get_cdn_policy()

        return None


class Settings(
    CTUIDModelMixin,
    models.Model,
):
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        related_name="settings",
    )
    debug_enabled = models.BooleanField(
        "enable debug",
        default=False,
        db_index=True,
    )
    testing_enabled = models.BooleanField(
        "enable testing",
        default=False,
        db_index=True,
    )
    news_provider = models.CharField(
        max_length=64,
        choices=NewsProvider.choices,
        default=NewsProvider.DISABLED,
        blank=True,
        db_index=True,
    )

    def __str__(self):
        return f"{self.ct}:{self.uid}"


class Address(
    CTUIDModelMixin,
    models.Model,
):
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        related_name="address",
    )
    line_1 = models.CharField(
        max_length=128,
        blank=True,
        default="",
    )
    line_2 = models.CharField(
        max_length=128,
        blank=True,
        default="",
    )
    postal_code = models.CharField(
        max_length=16,
        blank=True,
        default="",
    )
    city = models.CharField(
        max_length=128,
        blank=True,
        default="",
    )

    def __str__(self):
        return f"{self.ct}:{self.uid}"

    @property
    def country(self):
        return self.user.country


class LegacyUser(
    models.Model,
):
    email = models.EmailField(
        "Email address",
        unique=True,
        db_index=True,
    )
    obp_id = models.PositiveIntegerField(
        verbose_name="open broadcast - platform ID",
        db_index=True,
    )
    date_joined = models.DateTimeField(
        blank=True,
        null=True,
    )
    date_last_login = models.DateTimeField(
        blank=True,
        null=True,
    )
    first_name = models.CharField(
        max_length=64,
        default="",
        blank=True,
    )
    last_name = models.CharField(
        max_length=64,
        default="",
        blank=True,
    )
    phone = models.CharField(
        max_length=64,
        blank=True,
        default="",
        db_index=True,
    )
    gender = models.CharField(
        max_length=16,
        choices=GenderStr.choices,
        default=GenderStr.UNDEFINED,
        blank=True,
    )
    year_of_birth = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1900), MaxValueValidator(2022)],
    )
    is_listener = models.BooleanField(
        default=False,
        help_text="has account on radio site",
    )

    def __str__(self):
        return self.email

    def user(self):
        return User.objects.filter(obp_id=self.obp_id).first()


@receiver(pre_save, sender=User)
# pylint: disable=unused-argument
def user_pre_save(sender, instance, **kwargs):
    if legacy_user := LegacyUser.objects.filter(email=instance.email).first():
        instance.migration_source = MigrationSource.OBP
        instance.obp_id = legacy_user.obp_id

        for k in [
            "first_name",
            "last_name",
            "phone",
            "gender",
            "year_of_birth",
        ]:
            if not getattr(instance, k) and getattr(legacy_user, k):
                setattr(instance, k, getattr(legacy_user, k))


@receiver(post_save, sender=User)
# pylint: disable=unused-argument
def user_post_save(sender, instance, created, **kwargs):
    if not hasattr(instance, "settings"):
        Settings.objects.create(user=instance)

    if not hasattr(instance, "address"):
        Address.objects.create(user=instance)

    if created:
        account_signals.user_registered.send(
            sender=instance.__class__,
            user=instance,
        )


def get_default_token():
    token = token_login.generate_token()
    while LoginToken.objects.filter(value=token).exists():  # pragma: no cover
        token = token_login.generate_token()
    return token


class LoginTokenQuerySet(models.QuerySet):
    def valid(self):
        return self.filter(
            created__gt=timezone.now() - timedelta(hours=LOGIN_TOKEN_MAX_AGE),
        )

    def expired(self):
        return self.exclude(
            created__gt=timezone.now() - timedelta(hours=LOGIN_TOKEN_MAX_AGE),
        )


class LoginToken(
    CTUIDModelMixin,
):
    email = models.EmailField(
        "Email",
        db_index=True,
    )

    value = models.CharField(
        "Token",
        max_length=6,
        default=get_default_token,
        db_index=True,
        unique=True,
        editable=False,
    )

    created = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )

    claimed = models.DateTimeField(
        null=True,
        blank=True,
    )

    objects = LoginTokenQuerySet.as_manager()

    def __str__(self):
        return str(self.token_display)

    @property
    def token_display(self):
        bits = [
            self.value[0:3],
            self.value[3:6],
        ]
        return "-".join(bits)

    @property
    def is_valid(self):
        return self.created > timezone.now() - timedelta(hours=LOGIN_TOKEN_MAX_AGE)


class Theme(
    CTUIDModelMixin,
    models.Model,
):
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        related_name="theme",
    )
    css = models.TextField(
        "CSS",
        blank=True,
        default="",
    )

    def __str__(self):
        return f"{self.ct}:{self.uid}"


class GlobalPermissions(  # NOQA: DJ008
    models.Model,
):
    class Meta:
        managed = False
        default_permissions = ()

        permissions = (
            # sync
            ("api_sync_webhooks", "API - Sync webhooks"),
            # stats
            ("api_stats_view", "API - Stats view"),
            ("api_stats_webhooks", "API - Stats webhooks"),
            ("api_stats_event_create", "API - Stats create events"),
            # media / master download
            ("api_master_download", "API - Download media master files"),
        )
