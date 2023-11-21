from django.db import models

from common.models.mixins import CTUIDModelMixin, TimestampedModelMixin


class Category(
    CTUIDModelMixin,
    TimestampedModelMixin,
    models.Model,
):
    name = models.CharField(
        max_length=64,
    )
    priority = models.PositiveSmallIntegerField(
        default=0,
    )

    class Meta:
        app_label = "faq"
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = [
            "-priority",
            "name",
        ]

    def __str__(self):
        return self.name


class Topic(
    CTUIDModelMixin,
    TimestampedModelMixin,
    models.Model,
):
    question = models.TextField(
        max_length=256,
    )
    answer = models.TextField()
    priority = models.PositiveSmallIntegerField(
        default=0,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="topics",
    )

    class Meta:
        app_label = "faq"
        verbose_name = "Topic"
        ordering = [
            "category",
            "-priority",
            "question",
        ]

    def __str__(self):
        return self.question
