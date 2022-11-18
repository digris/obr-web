from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.functional import cached_property

from base.models.mixins import TimestampedModelMixin, CTUIDModelMixin
from broadcast.sync.editor import sync_editor
from image.models import BaseSortableImage
from sync.models.mixins import SyncModelMixin
from tagging.models import TaggedItem, TaggableManager


class Role(models.TextChoices):
    MUSIC_EDITOR = "music-editor", "Musikredaktion"


class Editor(
    TimestampedModelMixin,
    CTUIDModelMixin,
    SyncModelMixin,
    models.Model,
):
    display_name = models.CharField(
        verbose_name="Display name",
        max_length=256,
        null=True,
        blank=True,
    )

    location = models.CharField(
        verbose_name="Location",
        max_length=96,
        default="",
        blank=True,
    )

    description = models.TextField(
        verbose_name="Description",
        max_length=500,
        default="",
        blank=True,
    )

    user = models.OneToOneField(
        to="account.User",
        verbose_name="User account",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )

    tags = TaggableManager(
        through=TaggedItem,
        blank=True,
    )

    role = models.CharField(
        max_length=32,
        choices=Role.choices,
        default=Role.MUSIC_EDITOR,
    )

    is_active = models.BooleanField(
        default=False,
    )

    votes = GenericRelation(
        "rating.Vote",
        related_query_name="editor",
    )

    identifiers = GenericRelation(
        "identifier.Identifier",
        related_name="editor",
    )

    class Meta:
        app_label = "broadcast"
        verbose_name = "Editor"
        verbose_name_plural = "Editors"
        ordering = [
            "-is_active",
            "display_name",
        ]

    def __str__(self):
        return str(self.display_name or self.uid)

    def get_absolute_url(self):
        return f"/discover/editors/{self.uid}/"

    @cached_property
    def image(self):
        return self.images.first()

    @cached_property
    def is_former(self):
        return not self.is_active

    def sync_data(self, *args, **kwargs):
        return sync_editor(self, *args, **kwargs)


class EditorImage(BaseSortableImage):
    editor = models.ForeignKey(
        Editor,
        null=True,
        blank=False,
        related_name="images",
        on_delete=models.CASCADE,
    )

    class Meta:
        app_label = "broadcast"
        verbose_name = "Image"
        verbose_name_plural = "Images"
        ordering = ["position"]

    def __str__(self):
        return f"{self.pk}"
