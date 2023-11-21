from django.db import models
from django.urls import reverse

from base.models.mixins import CTUIDModelMixin, TimestampedModelMixin
from subscription import signals as subscription_signals


class PaymentProvider(models.TextChoices):
    STRIPE = "stripe", "Stripe"


class PaymentState(models.TextChoices):
    PENDING = "pending", "Pending"
    INITIALIZED = "initialized", "Initialized"
    PAID = "paid", "Paid"


class Payment(CTUIDModelMixin, TimestampedModelMixin, models.Model):
    state = models.CharField(
        verbose_name="State",
        max_length=32,
        db_index=True,
        choices=PaymentState.choices,
        default=PaymentState.PENDING,
    )

    provider = models.CharField(
        verbose_name="Provider",
        max_length=32,
        db_index=True,
        choices=PaymentProvider.choices,
        default=PaymentProvider.STRIPE,
    )

    transaction_id = models.CharField(
        verbose_name="Transaction ID",
        max_length=256,
        default="",
        blank=True,
        db_index=True,
    )

    amount = models.DecimalField(
        verbose_name="Amount paid",
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
        on_delete=models.CASCADE,
        related_name="payments",
    )

    extra_data = models.JSONField(
        null=True,
        blank=True,
    )

    class Meta:
        app_label = "subscription"
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
        ordering = ["-created"]

    def __str__(self):
        return f"{self.uid}"

    def get_api_url(self):
        return reverse(f"api:subscription:{self.provider}:endpoint")

    @property
    def is_paid(self):
        return self.state == PaymentState.PAID

    def set_state_paid(self, transaction_id, amount, currency):
        self.state = PaymentState.PAID
        self.transaction_id = transaction_id
        self.amount = amount
        self.currency = currency.upper()

        subscription_signals.payment_completed.send(
            sender=self.__class__,
            payment=self,
        )
