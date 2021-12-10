# -*- coding: utf-8 -*-
from django.contrib import admin

# sortable disabled for the moment. (wait for django 4 support)
# from adminsortable2.admin import SortableInlineAdminMixin


class SortableImageInlineMixin(admin.TabularInline):

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
