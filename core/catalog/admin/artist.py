# -*- coding: utf-8 -*-
from django.contrib import admin

from catalog.models.artist import Artist, ArtistImage
from identifier.admin import IdentifierInline
from image.admin import SortableImageInlineMixin
from image.utils import get_admin_inline_image


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
    readonly_fields = [
        "uuid",
        "uid",
        "tags",
    ]
    inlines = [
        ArtistImageInline,
        IdentifierInline,
    ]

    @admin.display(
        description="Image",
    )
    def image_display(self, obj):
        return get_admin_inline_image(obj)
