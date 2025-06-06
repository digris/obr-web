from django.db import models

from common.models.mixins import CTUIDModelMixin, TimestampedModelMixin


class SingleDonation(
    CTUIDModelMixin,
    TimestampedModelMixin,
    models.Model,
):

    class State(models.TextChoices):
        PENDING = "pending", "Pending"
        INITIALIZED = "initialized", "Initialized"
        SUCCEEDED = "succeeded", "Succeeded"
        FAILED = "failed", "Failed"

    state = models.CharField(
        verbose_name="State",
        max_length=32,
        db_index=True,
        choices=State.choices,
        default=State.PENDING,
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
        related_name="single_donations",
    )
    user_identity = models.CharField(
        max_length=64,
        default="",
        blank=True,
        db_index=True,
    )
    payment_intent_id = models.CharField(
        verbose_name="Stripe payment intent",
        max_length=256,
        default="",
        blank=True,
        db_index=True,
    )
    extra_data = models.JSONField(
        default=dict,
        blank=True,
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


class RecurringDonation(
    CTUIDModelMixin,
    TimestampedModelMixin,
    models.Model,
):

    class State(models.TextChoices):
        PENDING = "pending", "Pending"
        ACTIVE = "active", "Active"
        CANCELED = "canceled", "Canceled"
        EXPIRED = "expired", "Expired"
        FAILED = "failed", "Failed"

    state = models.CharField(
        verbose_name="State",
        max_length=32,
        db_index=True,
        choices=State.choices,
        default=State.PENDING,
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
    user = models.OneToOneField(
        to="account.User",
        on_delete=models.CASCADE,
        related_name="recurring_donation",
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
    )
    subscription_id = models.CharField(
        verbose_name="Stripe subscription",
        max_length=256,
        default="",
        blank=True,
        db_index=True,
    )
    extra_data = models.JSONField(
        default=dict,
        blank=True,
    )

    class Meta:
        app_label = "donation"
        verbose_name = "Donation (Recurring)"
        verbose_name_plural = "Donations (Recurring)"
        ordering = ["-created"]

    def __str__(self):
        return f"{self.uid}"

    @property
    def is_active(self):
        return self.state == self.State.ACTIVE

    # NOTE: not used at the moment
    def set_state_active(self, transaction_id, amount, currency):
        self.state = self.State.ACTIVE
        self.transaction_id = transaction_id
        self.amount = amount
        self.currency = currency.upper()
