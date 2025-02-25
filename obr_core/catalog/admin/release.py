from django.contrib import admin

from catalog.models.release import Release, ReleaseImage
from identifier.admin import IdentifierInline
from image.admin import SortableImageInlineMixin
from image.utils import get_admin_inline_image
from sync.admin import sync_qs_action


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
    raw_id_fields = [
        "label",
    ]
    inlines = [
        MediaArtistInline,
        ReleaseImageInline,
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

    @admin.display(
        description="Num. tracks",
    )
    def num_media(self, obj):  # pragma: no cover
        return obj.num_media
