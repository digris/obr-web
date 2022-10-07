from django.db import models
from django.db.models.functions import Now
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from base.models.mixins import CTUIDModelMixin, TimestampedModelMixin


class SubscriptionType(models.TextChoices):
    PLAN = "plan", "Plan"
    TRIAL = "trial", "Trial"


class SubscriptionQuerySet(models.QuerySet):
    def active(self):
        return self.filter(active_until__gte=Now())

    def expired(self):
        return self.filter(active_untill__lt=Now())


class SubscriptionManager(models.Manager):
    def get_queryset(self):
        return SubscriptionQuerySet(self.model, using=self._db)

    def get_for_user(self, user):
        if not user.is_authenticated:
            return None
        try:
            return self.get(user=user)
        except Subscription.DoesNotExist:
            return None


class Subscription(CTUIDModelMixin, TimestampedModelMixin, models.Model):

    type = models.CharField(
        max_length=16,
        db_index=True,
        default=SubscriptionType.PLAN,
        choices=SubscriptionType.choices,
    )

    active_until = models.DateTimeField(
        verbose_name="Valid until",
        db_index=True,
    )

    user = models.OneToOneField(
        to="account.User",
        on_delete=models.CASCADE,
        related_name="subscription",
    )

    # NOTE: preferred field type would be ArrayField - but then we cannot use sqlite for fast tests anymore
    countries_str = models.CharField(
        verbose_name="Countries",
        blank=True,
        max_length=64,
        default="CH",
        help_text="comma-separated, uppercase e.g. 'CH,FR'",
    )

    objects = SubscriptionManager()

    class Meta:
        app_label = "subscription"
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"

    @property
    def is_active(self):
        return self.active_until > timezone.now()

    @property
    def is_trial(self):
        return self.type == SubscriptionType.TRIAL

    @property
    def is_blocked(self):
        if self.user.country and self.user.country in self.countries:
            return False

        elif self.user.country:
            return _(f"Subscription not available in {self.user.country}")

        return _("Subscription blocked")

    @property
    def countries(self):
        return [c.strip().upper() for c in self.countries_str.split(",")]
