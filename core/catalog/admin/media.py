from django.contrib import admin
from django.db.models import Max

from catalog.models.media import Media, Airplay, Master
from identifier.admin import IdentifierInline
from sync.admin import sync_qs_action


class MediaArtistInline(admin.TabularInline):
    model = Media.artists.through
    raw_id_fields = ["artist"]
    extra = 0


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    save_on_top = True

    list_display = [
        "__str__",
        "uid",
        "artist_display",
        "duration",
        "latest_airplay",
        "num_airplays",
        "sync_state",
    ]
    list_filter = [
        "sync_state",
        "airplays__time_start",
        "releases__release_type",
    ]
    search_fields = [
        "name",
        "uid",
        "artists__name",
        "artists__uid",
    ]
    readonly_fields = [
        "uuid",
        "uid",
        "tags",
    ]
    inlines = [
        MediaArtistInline,
        IdentifierInline,
    ]
    actions = [
        sync_qs_action,
    ]

    def get_queryset(self, request):  # pragma: no cover
        qs = super().get_queryset(request)
        qs = qs.prefetch_related(
            "airplays",
            "media_artist",
            "media_artist__artist",
        )
        qs = qs.annotate(latest_airplay=Max("airplays__time_start"))
        return qs

    # def get_ordering(self, request):
    #     return ["-latest_airplay"]

    def latest_airplay(self, obj):  # pragma: no cover
        return obj.latest_airplay

    latest_airplay.admin_order_field = "latest_airplay"


@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    save_on_top = True

    list_display = [
        "media",
        "uid",
        "encoding",
        "content_type",
        "size",
        "path",
        "sync_state",
    ]
    list_filter = [
        "sync_state",
        "encoding",
        "content_type",
    ]
    search_fields = [
        "media__name",
        "media__uid",
        "md5_hash",
    ]
    readonly_fields = [
        "uid",
        "encoding",
        "md5_hash",
        "size",
        "content_type",
    ]
    raw_id_fields = [
        "media",
    ]
    actions = [
        sync_qs_action,
    ]


@admin.register(Airplay)
class AirplayAdmin(admin.ModelAdmin):
    save_on_top = True
    date_hierarchy = "time_start"
    list_display = [
        "media",
        "time_start",
        "time_end",
    ]
    search_fields = [
        "media__name",
        "media__uid",
        "media__uuid",
    ]
    raw_id_fields = [
        "media",
    ]
