from django.contrib import admin
from django.db.models import Count

import unfold.admin
import unfold.contrib.filters.admin
import unfold.decorators
from catalog.models.release import Release, ReleaseImage
from identifier.admin import IdentifierInline
from image.admin import SortableImageInlineMixin
from image.utils import get_admin_inline_image
from sync.admin import SyncAdminMixin, sync_qs_action


class ReleaseMediaInline(unfold.admin.TabularInline):
    model = Release.media.through
    autocomplete_fields = ["media"]
    extra = 0
    hide_title = True
    verbose_name = "Track"
    verbose_name_plural = "Tracks"


class ReleaseImageInline(SortableImageInlineMixin, unfold.admin.TabularInline):
    model = ReleaseImage


@admin.register(Release)
class ReleaseAdmin(SyncAdminMixin, unfold.admin.ModelAdmin):
    compressed_fields = True
    warn_unsaved_form = True
    list_fullwidth = True
    list_filter_sheet = False

    date_hierarchy = "created"
    list_display = [
        "image_display",
        "release_display",
        "label_display",
        "num_media_display",
        "sync_last_update",
        "sync_state_display",
        "uid_display",
    ]
    list_filter = [
        (
            "release_date",
            unfold.contrib.filters.admin.RangeDateFilter,
        ),
        "release_type",
        "label__kind",
        "sync_state",
    ]
    search_fields = [
        "name",
        "uid",
        "media__name",
        "media__uuid",
        "label__name",
        "label__uuid",
    ]
    readonly_fields = [
        "uuid",
        "uid",
        "tags",
    ]
    autocomplete_fields = [
        "label",
    ]
    inlines = [
        ReleaseMediaInline,
        ReleaseImageInline,
        IdentifierInline,
    ]
    actions = [
        sync_qs_action,
    ]

    def get_queryset(self, request):  # pragma: no cover
        qs = super().get_queryset(request)
        qs = qs.prefetch_related(
            "images",
        )
        qs = qs.annotate(
            num_media=Count(
                "media",
                distinct=True,
            ),
        )
        return qs

    ###################################################################
    # display
    ###################################################################
    @admin.display(
        description="Cover",
    )
    def image_display(self, obj):  # pragma: no cover
        return get_admin_inline_image(obj.image)

    @unfold.decorators.display(
        description="release",
        header=True,
        ordering="name",
    )
    def release_display(self, obj):
        lines = [obj.name]
        if obj.release_date:
            lines.append(
                f"{obj.release_date.year} - {obj.release_type.upper()}",
            )
        else:
            lines.append(obj.release_type.upper())
        return lines

    @unfold.decorators.display(
        description="label",
        header=True,
        ordering="label__name",
    )
    def label_display(self, obj):
        return obj.label or "-", obj.label.get_kind_display() if obj.label else "-"

    @admin.display(
        description="Num. tracks",
        ordering="num_media",
    )
    def num_media_display(self, obj):  # pragma: no cover
        return obj.num_media

    @unfold.decorators.display(
        description="UID",
        label=True,
    )
    def uid_display(self, obj):
        return obj.uid
