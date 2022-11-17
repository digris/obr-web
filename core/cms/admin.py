from django import forms
from django.contrib import admin
from django.db import models
from modeltranslation.admin import TranslationAdmin, TranslationStackedInline
from .models import Page, Section


class SectionAdminInline(
    TranslationStackedInline,
):
    model = Section
    extra = 0
    formfield_overrides = {
        models.TextField: {
            "widget": forms.Textarea(
                attrs={
                    "rows": 6,
                    "cols": 80,
                },
            )
        },
    }


@admin.register(Page)
class PageAdmin(
    TranslationAdmin,
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
                    "rows": 4,
                    "cols": 80,
                },
            )
        },
    }
