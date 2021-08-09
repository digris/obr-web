# -*- coding: utf-8 -*-
from adminsortable2.admin import SortableInlineAdminMixin

# from base.forms.widgets import ReadOnlyImageInput


class SortableImageInlineMixin(SortableInlineAdminMixin):

    extra = 0
    max_num = 10

    readonly_fields = [
        "colors",
    ]

    fields = [
        "file",
        "position",
        "colors",
    ]

    # formfield_overrides = {
    #     models.ImageField: {"widget": ReadOnlyImageInput},
    # }
