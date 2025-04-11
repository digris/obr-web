from datetime import timedelta

from django.contrib.sitemaps import Sitemap
from django.db.models import Count, Max, Q
from django.db.models.functions import Now

from catalog.models import Artist, Media

MEDIA_MIN_DURATION = 12
ARTIST_MIN_NUM_MEDIA = 1


class ArtistSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        qs = Artist.objects.all()
        qs = qs.prefetch_related(
            "media",
        )
        qs = qs.annotate(
            num_media=Count(
                "media",
                filter=Q(
                    media__airplays__time_start__lte=Now(),
                )
                & Q(
                    media__duration__gt=timedelta(seconds=MEDIA_MIN_DURATION),
                ),
                distinct=True,
            ),
        )
        qs = qs.filter(
            num_media__gte=ARTIST_MIN_NUM_MEDIA,
        )
        return qs

    def lastmod(self, obj):
        return obj.updated


class MediaSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        qs = Media.objects.all()
        qs = qs.annotate(
            latest_airplay=Max(
                "airplays__time_start",
                filter=Q(
                    airplays__time_start__lte=Now(),
                ),
            ),
        )
        qs = qs.filter(latest_airplay__lte=Now())
        return qs

    def lastmod(self, obj):
        return obj.updated
