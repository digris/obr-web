from django.contrib import admin

from catalog.models.label import Label, LabelImage
from identifier.admin import IdentifierInline
from image.admin import SortableImageInlineMixin
from image.utils import get_admin_inline_image
from sync.admin import sync_qs_action


class LabelImageInline(SortableImageInlineMixin, admin.TabularInline):
    model = LabelImage


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = [
        "image_display",
        "__str__",
        "uid",
        "num_releases",
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
        #
        "updated",
    ]
    inlines = [
        LabelImageInline,
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
        description="Num. releases",
    )
    def num_releases(self, obj):  # pragma: no cover
        return obj.num_releases
