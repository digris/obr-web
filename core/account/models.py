from datetime import timedelta

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from django_countries.fields import CountryField

from account import signals as account_signals
from account import token_login
from account.settings import LOGIN_TOKEN_MAX_AGE
from account.sync.user import sync_user
from base.models.mixins import CTUIDModelMixin
from sync.models.mixins import SyncModelMixin


class MigrationSource(models.TextChoices):
    EMPTY = "", "none"
    OBR = "obr", "OBR - radio"
    OBP = "obp", "OBP - platform"


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
            raise ValueError(_("The Email must be set"))
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
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


class User(
    CTUIDModelMixin,
    SyncModelMixin,
    AbstractBaseUser,
    PermissionsMixin,
):
    email = models.EmailField(
        _("email address"),
        unique=True,
    )
    first_name = models.CharField(
        max_length=64,
        null=True,
        blank=True,
    )
    last_name = models.CharField(
        max_length=64,
        null=True,
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
        return hasattr(self, "subscription") and self.subscription.is_active


class Settings(
    CTUIDModelMixin,
    models.Model,
):

    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        related_name="settings",
    )


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

    country = CountryField(
        blank=True,
        null=True,
    )


@receiver(post_save, sender=User)
# pylint: disable=unused-argument
def create_user_settings(sender, instance, created, **kwargs):

    if created and not hasattr(instance, "settings"):
        Settings.objects.create(user=instance)

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
        _("email"),
        db_index=True,
    )

    value = models.CharField(
        _("token"),
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
