# -*- coding: utf-8 -*-
from django.contrib import admin

from catalog.models.release import Release, ReleaseImage
from identifier.admin import IdentifierInline
from image.admin import SortableImageInlineMixin
from image.utils import get_admin_inline_image


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
        "num_media",
        # "created",
        # "updated",
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
        "media__name",
        "media__uuid",
    ]
    readonly_fields = [
        "uuid",
        "uid",
        "tags",
    ]
    inlines = [
        MediaArtistInline,
        ReleaseImageInline,
        IdentifierInline,
    ]

    @admin.display(
        description="Image",
    )
    def image_display(self, obj):
        return get_admin_inline_image(obj)

    @admin.display(
        description="Num. tracks",
    )
    def num_media(self, obj):
        return obj.num_media
