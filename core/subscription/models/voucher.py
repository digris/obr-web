import random
import string
from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone

from base.models.mixins import CTUIDModelMixin, TimestampedModelMixin


def generate_code(num_chars=6):
    chars = string.ascii_uppercase
    return "".join(random.SystemRandom().choice(chars) for _ in range(num_chars))


def get_default_code():
    code = generate_code()
    while Voucher.objects.filter(code=code).exists():  # pragma: no cover
        code = generate_code()
    return code


def get_default_valid_until():
    return timezone.now() + timedelta(days=365)


class Voucher(CTUIDModelMixin, TimestampedModelMixin, models.Model):

    code = models.CharField(
        max_length=6,
        default=get_default_code,
        unique=True,
        null=False,
        blank=False,
        db_index=True,
        editable=False,
    )

    num_days = models.PositiveIntegerField(
        default=7,
        null=False,
        blank=False,
    )

    valid_until = models.DateTimeField(
        default=get_default_valid_until,
        db_index=True,
    )

    max_num_use = models.PositiveIntegerField(
        blank=True,
        null=True,
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Owner",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="vouchers",
    )

    class Meta:
        app_label = "subscription"
        verbose_name = "Voucher"
        verbose_name_plural = "Voucher"

    def __str__(self):
        return str(self.code_display)

    @property
    def code_display(self):
        bits = [
            self.code[0:2],
            self.code[2:4],
            self.code[4:6],
        ]
        return "-".join(bits)

    @property
    def num_used(self):
        return self.redemtions.count()

    @property
    def is_valid(self):

        if self.valid_until < timezone.now():
            return False

        if self.max_num_use and self.num_used >= self.max_num_use:
            return False

        return True

    # @property
    # def is_valid_for_user(self):
    #     return False

    # is_valid_for_user = False

    # def save(self, *args, **kwargs):
    #     if not self.code:
    #         # pylint: disable=unused-variable
    #         for i in itertools.count(1):
    #             code = generate_code()
    #             if not Voucher.objects.filter(code=code).exists():
    #                 self.code = code
    #                 break
    #     return super().save(*args, **kwargs)


class Redemption(CTUIDModelMixin, TimestampedModelMixin, models.Model):

    voucher = models.ForeignKey(
        Voucher,
        related_name="redemtions",
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        "account.User",
        related_name="redemtions",
        on_delete=models.CASCADE,
    )

    class Meta:
        app_label = "subscription"
        verbose_name = "Redemption"
        verbose_name_plural = "Redemptions"
        unique_together = [
            "voucher",
            "user",
        ]

    def __str__(self):
        return f"{self.voucher} - {self.user}"
