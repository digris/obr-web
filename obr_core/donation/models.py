from django.db import models

from common.models.mixins import CTUIDModelMixin, TimestampedModelMixin


class Donation(
    CTUIDModelMixin,
    TimestampedModelMixin,
    models.Model,
):

    class Kind(models.TextChoices):
        SINGLE = "single", "Single"
        RECURRING = "recurring", "Recurring"

    class State(models.TextChoices):
        PENDING = "pending", "Pending"
        FAILED = "failed", "Failed"
        # single
        SUCCEEDED = "succeeded", "Succeeded"
        # recurring
        ACTIVE = "active", "Active"
        CANCELED = "canceled", "Canceled"
        EXPIRED = "expired", "Expired"

    class ClientMode(models.TextChoices):
        WEB = "web", "Web"
        APP = "app", "App"

    kind = models.CharField(
        verbose_name="Kind",
        max_length=16,
        db_index=True,
        choices=Kind.choices,
        default=Kind.SINGLE,
    )
    state = models.CharField(
        verbose_name="State",
        max_length=16,
        db_index=True,
        choices=State.choices,
        default=State.PENDING,
    )
    client_mode = models.CharField(
        verbose_name="Client mode",
        max_length=16,
        db_index=True,
        choices=ClientMode.choices,
        default=ClientMode.WEB,
    )
    amount = models.DecimalField(
        verbose_name="Amount",
        max_digits=10,
        decimal_places=3,
    )
    currency = models.CharField(
        verbose_name="Currency",
        max_length=3,
        default="CHF",
    )
    user = models.ForeignKey(
        to="account.User",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="donations",
    )
    user_identity = models.CharField(
        max_length=64,
        default="",
        blank=True,
        db_index=True,
        help_text="only used for single donations (anonymous users)",
    )
    payment_intent_id = models.CharField(
        verbose_name="Stripe payment intent",
        max_length=256,
        default="",
        blank=True,
        db_index=True,
    )
    price_id = models.CharField(
        verbose_name="Stripe price",
        max_length=256,
        default="",
        blank=True,
        db_index=True,
        help_text="only used for recurring donations",
    )
    subscription_id = models.CharField(
        verbose_name="Stripe subscription",
        max_length=256,
        default="",
        blank=True,
        db_index=True,
        help_text="only used for recurring donations",
    )
    payment_intent_data = models.JSONField(
        default=dict,
        blank=True,
    )
    subscription_data = models.JSONField(
        default=dict,
        blank=True,
        help_text="only used for recurring donations",
    )

    class Meta:
        app_label = "donation"
        verbose_name = "Donation"
        verbose_name_plural = "Donations"
        ordering = ["-created"]

    def __str__(self):
        return f"{self.uid}"

    @property
    def is_paid(self):
        return self.state == self.State.SUCCEEDED

    # NOTE: not used at the moment
    def set_state_paid(self, transaction_id, amount, currency):
        self.state = self.State.SUCCEEDED
        self.transaction_id = transaction_id
        self.amount = amount
        self.currency = currency.upper()


# class RecurringDonation(
#     CTUIDModelMixin,
#     TimestampedModelMixin,
#     models.Model,
# ):
#
#     class State(models.TextChoices):
#
#
#     class Meta:
#
#     def __str__(self):
#
#     @property
#     def is_active(self):
#
#     def set_state_active(self, transaction_id, amount, currency):
