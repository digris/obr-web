from django.contrib import admin
from catalog.models import Media, MediaArtists


class MediaArtistInline(admin.TabularInline):
    model = Media.artists.through
    raw_id_fields = ["artist"]
    extra = 0


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    save_on_top = True

    inlines = [
        MediaArtistInline,
    ]

    list_display = [
        "__str__",
        "artist_display",
        "duration",
    ]
