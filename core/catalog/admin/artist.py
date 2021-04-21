# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.safestring import mark_safe

from catalog.models.artist import Artist, ArtistImage
from image.admin import SortableImageInlineMixin


class ArtistImageInline(SortableImageInlineMixin, admin.TabularInline):
    model = ArtistImage


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
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
        "uid",
    ]
    inlines = [
        ArtistImageInline,
    ]

    def image_display(self, obj):
        if not (obj.image and obj.image.file):
            return "-"
        return mark_safe('<img width="100" src="{url}"/>'.format(url=obj.image.url))

    image_display.short_description = "Image"
