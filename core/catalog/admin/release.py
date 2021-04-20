# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.safestring import mark_safe
from catalog.models.release import Release, ReleaseImage
from image.admin import SortableImageInlineMixin


class MediaArtistInline(admin.TabularInline):
    model = Release.media.through
    raw_id_fields = ["media"]
    extra = 0


class ReleaseImageInline(SortableImageInlineMixin, admin.TabularInline):
    model = ReleaseImage


@admin.register(Release)
class ReleaseAdmin(admin.ModelAdmin):
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
        MediaArtistInline,
        ReleaseImageInline,
    ]

    def image_display(self, obj):
        if not (obj.image and obj.image.file):
            return "-"
        return mark_safe('<img width="100" src="{url}"/>'.format(url=obj.image.url))

    image_display.short_description = "Image"
