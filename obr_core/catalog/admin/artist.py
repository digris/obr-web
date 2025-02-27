from django.contrib import admin
from django.utils.safestring import mark_safe

import unfold.admin
import unfold.contrib.filters.admin
import unfold.decorators
from catalog.models.artist import Artist, ArtistImage
from identifier.admin import IdentifierInline
from image.admin import SortableImageInlineMixin
from image.utils import get_admin_inline_image
from sync.admin import SyncAdminMixin, sync_qs_action


class ArtistImageInline(SortableImageInlineMixin, unfold.admin.TabularInline):
    model = ArtistImage


@admin.register(Artist)
class ArtistAdmin(SyncAdminMixin, unfold.admin.ModelAdmin):
    compressed_fields = True
    warn_unsaved_form = True
    list_fullwidth = True
    list_filter_sheet = False

    date_hierarchy = "created"
    list_display = [
        "image_display",
        "artist_display",
        "timespan_display",
        "num_media_display",
        "sync_last_update",
        "sync_state_display",
        "uid_display",
    ]
    list_filter = [
        "sync_state",
    ]
    search_fields = [
        "name",
        "uid",
    ]
    readonly_fields = [
        "uuid",
        "uid",
        "tags",
    ]
    inlines = [
        ArtistImageInline,
        IdentifierInline,
    ]
    actions = [
        sync_qs_action,
    ]

    ###################################################################
    # display
    ###################################################################
    @admin.display(
        description="Image",
    )
    def image_display(self, obj):  # pragma: no cover
        return get_admin_inline_image(obj.image)

    @unfold.decorators.display(
        description="artist",
        header=True,
        ordering="name",
    )
    def artist_display(self, obj):
        return obj.name, obj.country_code or "-"

    @admin.display(
        description="Timespan",
    )
    def timespan_display(self, obj):  # pragma: no cover
        html = ""
        if obj.date_start:
            html += f"<sup>*</sup><span>{obj.date_start.year}</span>"
        if obj.date_start and obj.date_end:
            html += " &ndash; "
        if obj.date_end:
            html += f"<sup>✝</sup><span>{obj.date_end.year}</span>"
        return mark_safe(html.strip() or "-")  # NOQA S308

    @admin.display(
        description="Num. tracks",
    )
    def num_media_display(self, obj):  # pragma: no cover
        return obj.num_media

    @unfold.decorators.display(
        description="UID",
        label=True,
    )
    def uid_display(self, obj):
        return obj.uid
