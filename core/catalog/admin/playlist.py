from django.contrib import admin

from catalog.models.playlist import Playlist, PlaylistImage, Series
from image.admin import SortableImageInlineMixin
from image.utils import get_admin_inline_image
from sync.admin import sync_qs_action


class PlaylistMediaInline(admin.TabularInline):
    model = Playlist.media.through
    raw_id_fields = ["media"]
    extra = 0


class PlaylistImageInline(SortableImageInlineMixin, admin.TabularInline):
    model = PlaylistImage


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = [
        "name",
        "num_playlists",
        "sync_state",
    ]
    list_filter = [
        "updated",
        "sync_state",
    ]


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = [
        "image_display",
        "name",
        "series_display",
        "editor",
        "uid",
        "sync_state",
    ]
    list_filter = [
        "updated",
        "sync_state",
        "editor",
        "series",
    ]
    search_fields = [
        "name",
        "uid",
        "series__uid",
        "series__name",
        "editor__uid",
        "editor__display_name",
    ]
    readonly_fields = [
        "series",
        "series_episode",
        "editor",
        "uuid",
        "uid",
        "tags",
    ]
    date_hierarchy = "created"
    inlines = [
        PlaylistMediaInline,
        PlaylistImageInline,
    ]
    actions = [
        sync_qs_action,
    ]
    raw_id_fields = [
        "editor",
        "series",
    ]

    @admin.display(
        empty_value="-",
        ordering="series__name",
        description="Series",
    )
    def series_display(self, obj):  # pragma: no cover
        if obj.series and obj.series_episode:
            return f"{obj.series.name} #{obj.series_episode}"
        if obj.series:
            return obj.series.name
        return None

    @admin.display(
        description="Image",
    )
    def image_display(self, obj):  # pragma: no cover
        return get_admin_inline_image(obj)
