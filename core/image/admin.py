from django.contrib import admin
from django.utils.safestring import mark_safe

from .utils import get_admin_inline_image

# sortable disabled for the moment. (wait for django 4 support)
# from adminsortable2.admin import SortableInlineAdminMixin


class SortableImageInlineMixin(
    # SortableInlineAdminMixin,
    admin.TabularInline,
):

    extra = 0
    max_num = 10

    readonly_fields = [
        "image_display",
        "color_display",
    ]

    fields = [
        "image_display",
        "file",
        "color_display",
        "position",
    ]

    # formfield_overrides = {
    #     models.ImageField: {"widget": ReadOnlyImageInput},
    # }

    @admin.display(
        description="Image",
    )
    def image_display(self, obj):  # pragma: no cover
        return get_admin_inline_image(obj)

    @admin.display(
        description="Color",
        empty_value="-",
    )
    def color_display(self, obj):
        if not obj.colors:
            return None
        if primary := obj.colors.get("primary"):
            c0 = " ".join([str(b) for b in primary])
            style = f"background: rgb({c0}); width:80px; height:80px;"
            return mark_safe(f'<div style="{style}"></div>')
        return None
