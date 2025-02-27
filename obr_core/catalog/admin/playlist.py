from django.contrib import admin
from django.db.models import Count, Max, Q
from django.db.models.functions import Coalesce, Now

import unfold.admin
import unfold.contrib.filters.admin
import unfold.decorators
from adminsortable2.admin import SortableAdminBase, SortableInlineAdminMixin
from catalog.models.playlist import Playlist, PlaylistImage, Series
from image.admin import SortableImageInlineMixin
from image.utils import get_admin_inline_image
from sync.admin import SyncAdminMixin, sync_qs_action


class PlaylistMediaInline(
    unfold.admin.TabularInline,
):
    model = Playlist.media.through
    autocomplete_fields = ["media"]
    extra = 0
    readonly_fields = [
        "duration",
    ]
    hide_title = True

    @admin.display(
        empty_value="-",
        description="Duration",
    )
    def duration(self, obj):  # pragma: no cover
        if obj.media and obj.media.duration:
            return obj.media.duration.seconds
        return None


class PlaylistImageInline(
    SortableImageInlineMixin,
    SortableInlineAdminMixin,
    unfold.admin.TabularInline,
):
    model = PlaylistImage


@admin.register(Series)
class SeriesAdmin(
    SyncAdminMixin,
    unfold.admin.ModelAdmin,
):
    compressed_fields = True
    warn_unsaved_form = True
    list_fullwidth = True

    list_display = [
        "name",
        "num_playlists_display",
        "sync_last_update",
        "sync_state_display",
        "uid_display",
    ]
    list_filter = [
        "updated",
        "sync_state",
    ]
    search_fields = [
        "name",
        "uid",
    ]

    def get_queryset(self, request):  # pragma: no cover
        qs = super().get_queryset(request)
        qs = qs.annotate(
            num_playlists=Count("playlists"),
        )
        return qs

    ###################################################################
    # display
    ###################################################################
    @unfold.decorators.display(
        description="Num. playlists",
        ordering="num_playlists",
    )
    def num_playlists_display(self, obj):
        return obj.num_playlists

    @unfold.decorators.display(
        description="UID",
        label=True,
    )
    def uid_display(self, obj):
        return obj.uid


@admin.register(Playlist)
class PlaylistAdmin(
    SyncAdminMixin,
    SortableAdminBase,
    unfold.admin.ModelAdmin,
):
    compressed_fields = True
    warn_unsaved_form = True
    list_fullwidth = True
    list_filter_sheet = False

    list_display = [
        "image_display",
        "playlist_display",
        "editor",
        "num_emissions_display",
        "last_emission_display",
        "sync_last_update",
        "sync_state_display",
        "uid_display",
    ]
    list_filter = [
        "updated",
        "sync_state",
        "sync_last_update",
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

    def get_queryset(self, request):  # pragma: no cover
        qs = super().get_queryset(request)
        qs = qs.select_related(
            "series",
            "editor",
        ).prefetch_related(
            "images",
        )
        qs = qs.annotate(
            last_emission=Max(
                "emissions__time_start",
                filter=Q(emissions__time_start__lt=Now()),
            ),
            num_emissions=Coalesce(
                Count(
                    "emissions",
                    distinct=True,
                    filter=Q(emissions__time_start__lt=Now()),
                ),
                0,
            )
            + Coalesce(
                Count("archived_emissions", distinct=True),
                0,
            ),
        )
        return qs

    ###################################################################
    # extra templates
    ###################################################################
    change_form_after_template = "catalog/admin/playlist_after.html"

    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        extra_context = extra_context or {}
        obj = self.get_object(request, object_id)

        extra_context.update(
            {
                "emissions_table": {
                    "headers": ["time start"],
                    "rows": list(obj.emissions.values_list("time_start"))
                    + list(obj.archived_emissions.values_list("time_start")),
                },
            },
        )
        return super().changeform_view(request, object_id, form_url, extra_context)

    ###################################################################
    # display
    ###################################################################
    @unfold.decorators.display(
        description="playlist",
        header=True,
        ordering="name",
    )
    def playlist_display(self, obj):
        lines = [obj.name]
        if obj.series and obj.series_episode:
            lines.append(f"{obj.series.name} #{obj.series_episode}")
        elif obj.series:
            lines.append(obj.series.name)
        else:
            lines.append("-")
        return lines

    @admin.display(
        description="Image",
    )
    def image_display(self, obj):  # pragma: no cover
        return get_admin_inline_image(obj.image)

    @unfold.decorators.display(
        description="emissions",
        ordering="num_emissions",
    )
    def num_emissions_display(self, obj):
        return obj.num_emissions

    @unfold.decorators.display(
        description="last emission",
        ordering="last_emission",
    )
    def last_emission_display(self, obj):
        return obj.last_emission

    @unfold.decorators.display(
        description="UID",
        label=True,
    )
    def uid_display(self, obj):
        return obj.uid
