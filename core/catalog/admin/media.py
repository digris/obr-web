from django.contrib import admin
from django.db.models import Max

from catalog.models.media import Media, Airplay
from identifier.admin import IdentifierInline


class MediaArtistInline(admin.TabularInline):
    model = Media.artists.through
    raw_id_fields = ["artist"]
    extra = 0


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    save_on_top = True

    inlines = [
        MediaArtistInline,
        IdentifierInline,
    ]

    list_display = [
        "__str__",
        "uid",
        "artist_display",
        "duration",
        # "created",
        # "updated",
        "latest_airplay",
        "num_airplays",
        "sync_state",
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

    def get_queryset(self, request):
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

    def latest_airplay(self, obj):
        return obj.latest_airplay

    latest_airplay.admin_order_field = "latest_airplay"


@admin.register(Airplay)
class AirplayAdmin(admin.ModelAdmin):
    save_on_top = True

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

    date_hierarchy = "time_start"
