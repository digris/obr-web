# -*- coding: utf-8 -*-
from adminsortable2.admin import SortableInlineAdminMixin
from django.db import models
from parler.admin import TranslatableInlineModelAdmin

from base.forms.widgets import ReadOnlyImageInput


class SortableImageInlineMixin(SortableInlineAdminMixin, TranslatableInlineModelAdmin):

    extra = 0
    max_num = 10

    fields = ["file", "position", "caption"]

    formfield_overrides = {
        models.ImageField: {"widget": ReadOnlyImageInput},
    }
