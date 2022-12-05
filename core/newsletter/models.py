from django.db import models
from base.models.mixins import TimestampedModelMixin, CTUIDModelMixin


class Newsletter(
    CTUIDModelMixin,
    TimestampedModelMixin,
    models.Model,
):
    title = models.CharField(
        max_length=64,
    )
    description = models.TextField(
        max_length=256,
        blank=True,
        default="",
    )

    class Meta:
        app_label = "newsletter"
        verbose_name = "Newsletter"
        verbose_name_plural = "Newsletters"
        ordering = [
            "title",
        ]

    def __str__(self):
        return self.title


class Subscription(
    CTUIDModelMixin,
    TimestampedModelMixin,
    models.Model,
):
    newsletter = models.ForeignKey(
        Newsletter,
        on_delete=models.CASCADE,
        related_name="subscriptions",
    )

    user = models.ForeignKey(
        to="account.User",
        on_delete=models.CASCADE,
        related_name="newsletter_subscriptions",
    )

    class Meta:
        app_label = "newsletter"
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"

    def __str__(self):
        return f"{self.newsletter} - {self.user}"