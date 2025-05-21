import json
from datetime import date, datetime, timedelta

from django.contrib import admin
from django.db.models import Count, Max, Q
from django.db.models.functions import Coalesce
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe
from django.utils.timezone import make_aware

import qsstats
import unfold.admin
import unfold.decorators
from catalog.models.license import LicenseKind
from catalog.models.media import Airplay, Master, Media
from catalog.models.release import Release
from identifier.admin import IdentifierInline
from image.utils import get_admin_inline_image
from sync.admin import SyncAdminMixin, sync_qs_action

AGGREGATE_MAX_AGE = make_aware(datetime.combine(date(2024, 1, 1), datetime.min.time()))


class MediaArtistInline(unfold.admin.TabularInline):
    model = Media.artists.through
    autocomplete_fields = ["artist"]
    extra = 0
    hide_title = True
    verbose_name = "Artist"
    verbose_name_plural = "Artists"


class MediaReleaseInline(unfold.admin.TabularInline):
    model = Release.media.through
    autocomplete_fields = ["release"]
    extra = 0
    hide_title = True
    verbose_name = "Release"
    verbose_name_plural = "Releases"


@admin.register(Media)
class MediaAdmin(SyncAdminMixin, unfold.admin.ModelAdmin):
    compressed_fields = True
    warn_unsaved_form = True
    list_fullwidth = True
    list_filter_sheet = False

    list_display = [
        "image_display",
        "media_display",
        "release_display",
        "kind",
        "duration_display",
        # "rating_display",
        # "num_airplays_display",
        # "latest_airplay_display",
        "identifiers_display",
        "lyrics_display",
        "license_display",
        # "sync_last_update",
        "sync_state_display",
        "uid_display",
    ]
    list_filter = [
        # "sync_last_update",
        # "kind",
        "license",
        "lyrics_explicit",
        "sync_state",
        "identifiers__scope",
    ]
    search_fields = [
        "name",
        "uid",
        "artists__name",
        "artists__uid",
        "releases__name",
        "releases__uid",
        "releases__label__name",
        "releases__label__uid",
        "identifiers__value",
    ]
    readonly_fields = [
        "uuid",
        "uid",
        "tags",
        "license",
    ]
    inlines = [
        MediaArtistInline,
        MediaReleaseInline,
        IdentifierInline,
    ]
    actions = [
        sync_qs_action,
    ]

    def get_queryset(self, request):  # pragma: no cover
        qs = super().get_queryset(request)
        qs = qs.select_related(
            "master",
        ).prefetch_related(
            "airplays",
            "media_artist",
            "media_artist__artist",
            "releases",
            "releases__images",
            "releases__label",
            "votes",
        )
        qs.annotate(
            latest_airplay=Max("airplays__time_start"),
            num_votes=Count(
                "votes",
                distinct=True,
                filter=Q(votes__created__gte=AGGREGATE_MAX_AGE),
            ),
            num_votes_up=Count(
                "votes",
                distinct=True,
                filter=Q(votes__value__gte=1, votes__created__gte=AGGREGATE_MAX_AGE),
            ),
            num_votes_down=Count(
                "votes",
                distinct=True,
                filter=Q(votes__value__lte=-1, votes__created__gte=AGGREGATE_MAX_AGE),
            ),
            num_airplays=Coalesce(
                Count(
                    "airplays",
                    airplays__created__gte=AGGREGATE_MAX_AGE,
                    distinct=True,
                ),
                0,
            )
            + Coalesce(
                Count(
                    "archived_airplays",
                    archived_airplays__created__gte=AGGREGATE_MAX_AGE,
                    distinct=True,
                ),
                0,
            ),
        )
        return qs

    ###################################################################
    # extra templates
    ###################################################################
    change_form_after_template = "catalog/admin/media_after.html"

    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        extra_context = extra_context or {}
        obj = self.get_object(request, object_id)

        today = date.today()

        qss = qsstats.QuerySetStats(obj.airplays.all(), "time_start")
        qss_archived = qsstats.QuerySetStats(obj.archived_airplays.all(), "time_start")

        ts = qss.time_series(today - timedelta(days=365), today, interval="months")
        ts_archived = qss_archived.time_series(
            today - timedelta(days=365),
            today,
            interval="months",
        )

        labels = [f"{d[0]:%b. %Y}" for d in ts]
        values = [d[1] for d in ts]
        values_archived = [d[1] for d in ts_archived]

        data = [x + y for x, y in zip(values, values_archived, strict=True)]

        extra_context.update(
            {
                "airplays_chart": json.dumps(
                    {
                        "labels": labels,
                        "datasets": [
                            {
                                "data": data,
                                "backgroundColor": "var(--color-primary-600)",
                            },
                        ],
                    },
                ),
            },
        )
        return super().changeform_view(request, object_id, form_url, extra_context)

    ###################################################################
    # display
    ###################################################################
    @admin.display(
        description="Cover",
    )
    def image_display(self, obj):  # pragma: no cover
        if obj.releases.exists():
            return get_admin_inline_image(obj.releases.first().images.first())
        return None

    @unfold.decorators.display(
        description="media",
        header=True,
        ordering="name",
    )
    def media_display(self, obj):
        return obj.name, obj.artist_display

    @unfold.decorators.display(
        description="release",
        header=True,
        ordering="releases__name",
    )
    def release_display(self, obj):
        return obj.release or "-", (
            obj.release.label if obj.release and obj.release.label else "-"
        )

    @unfold.decorators.display(
        description="duration",
        ordering="duration",
    )
    def duration_display(self, obj):
        return timedelta(seconds=obj.duration.seconds)

    @unfold.decorators.display(
        description="rating",
        ordering="num_votes",
    )
    def rating_display(self, obj):
        return mark_safe(  # NOQA S308
            f"<span>{obj.num_votes_up}</span> &ndash; <span>{obj.num_votes_down}</span>",
        )

    @unfold.decorators.display(
        description="airplays",
        ordering="num_airplays",
    )
    def num_airplays_display(self, obj):
        return obj.num_airplays

    @unfold.decorators.display(
        description="latest airplay",
        ordering="latest_airplay",
    )
    def latest_airplay_display(self, obj):
        return obj.latest_airplay

    @unfold.decorators.display(
        description="Lyrics",
        ordering="lyrics_explicit",
        label={
            Media.LyricsExplicit.CLEAN: "success",
            Media.LyricsExplicit.EXPLICIT: "warning",
        },
    )
    def lyrics_display(self, obj):
        return obj.lyrics_explicit

    @unfold.decorators.display(
        description="license",
        ordering="license",
        label={
            LicenseKind.UNKNOWN: None,
            LicenseKind.INDEPENDENT: "success",
            LicenseKind.MAJOR: "warning",
            LicenseKind.MAJOR_ROOT: "warning",
        },
    )
    def license_display(self, obj):
        return obj.license

    @unfold.decorators.display(
        description="Identifiers",
        label=True,
    )
    def identifiers_display(self, obj):
        return [i.get_scope_display() for i in obj.identifiers.all()]

    @unfold.decorators.display(
        description="UID",
        label=True,
    )
    def uid_display(self, obj):
        return obj.uid

    fieldsets = [
        (
            None,
            {
                "fields": [
                    "sync_state",
                    "name",
                    "duration",
                    "kind",
                    "license",
                    "uuid",
                    "uid",
                    "tags",
                ],
            },
        ),
    ]


@admin.register(Master)
class MasterAdmin(unfold.admin.ModelAdmin):
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
class AirplayAdmin(unfold.admin.ModelAdmin):
    save_on_top = True
    date_hierarchy = "time_start"
    list_display = [
        "media_display",
        "time_start",
        "time_end",
        "duration",
    ]
    search_fields = [
        "media__name",
        "media__uid",
        "media__uuid",
    ]
    raw_id_fields = [
        "media",
    ]

    ###################################################################
    # display
    ###################################################################
    @unfold.decorators.display(
        description="media",
        header=True,
        ordering="media__name",
    )
    def media_display(self, obj):
        return obj.media, obj.media.artist_display if obj.media else "-"
