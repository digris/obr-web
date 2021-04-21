# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.safestring import mark_safe

from catalog.models.playlist import Playlist, PlaylistImage
from image.admin import SortableImageInlineMixin


class PlaylistMediaInline(admin.TabularInline):
    model = Playlist.media.through
    raw_id_fields = ["media"]
    extra = 0


class PlaylistImageInline(SortableImageInlineMixin, admin.TabularInline):
    model = PlaylistImage


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = [
        "image_display",
        "__str__",
        "uid",
        "created",
        "updated",
        "sync_state",
    ]
    list_filter = [
        "created",
        "updated",
        "sync_state",
    ]
    search_fields = [
        "name",
    ]
    date_hierarchy = "created"
    inlines = [
        PlaylistMediaInline,
        PlaylistImageInline,
    ]

    def image_display(self, obj):
        if not (obj.image and obj.image.file):
            return "-"
        return mark_safe('<img width="100" src="{url}"/>'.format(url=obj.image.url))

    image_display.short_description = "Image"
