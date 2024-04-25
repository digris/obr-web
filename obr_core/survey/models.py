from django.conf import settings
from django.db import models

from common.models.mixins import CTUIDModelMixin, TimestampedModelMixin


class NewsSurveySubmission(
    CTUIDModelMixin,
    TimestampedModelMixin,
    models.Model,
):
    is_interested = models.BooleanField(
        default=False,
        db_index=True,
    )
    news_sources = models.JSONField(
        default=list,
    )
    comment = models.TextField(
        blank=True,
        default="",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="+",
    )
    user_identity = models.CharField(
        max_length=64,
        default="",
        blank=True,
        db_index=True,
    )

    class Meta:
        app_label = "survey"
        verbose_name = "News Survey Submission"
        verbose_name_plural = "News Survey Submission"

    def __str__(self):
        return str(self.uid)
