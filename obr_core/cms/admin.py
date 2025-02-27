from django import forms
from django.contrib import admin
from django.db import models

import unfold.admin
import unfold.decorators
from modeltranslation.admin import TabbedTranslationAdmin, TranslationStackedInline

from .models import Page, Section


class SectionAdminInline(
    unfold.admin.StackedInline,
    TranslationStackedInline,
):
    model = Section
    extra = 0


@admin.register(Page)
class PageAdmin(
    unfold.admin.ModelAdmin,
    TabbedTranslationAdmin,
):
    save_on_top = True
    list_display = [
        "__str__",
        "path",
        "uid",
    ]
    search_fields = [
        "title",
        "path",
    ]
    list_filter = [
        "created",
        "updated",
    ]
    inlines = [
        SectionAdminInline,
    ]
    formfield_overrides = {
        models.TextField: {
            "widget": forms.Textarea(
                attrs={
                    "rows": 6,
                    "cols": 80,
                },
            ),
        },
    }
