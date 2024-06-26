from django.contrib import admin

from catalog.models.artist import Artist, ArtistImage
from identifier.admin import IdentifierInline
from image.admin import SortableImageInlineMixin
from image.utils import get_admin_inline_image
from sync.admin import sync_qs_action


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
        "sync_last_update",
    ]
    list_filter = [
        "created",
        "updated",
        "sync_state",
        "sync_last_update",
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
    actions = [
        sync_qs_action,
    ]

    @admin.display(
        description="Image",
    )
    def image_display(self, obj):  # pragma: no cover
        return get_admin_inline_image(obj.image)
