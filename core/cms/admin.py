from django.contrib import admin

from modeltranslation.admin import TranslationAdmin, TranslationStackedInline
from .models import Page, Section


class SectionAdminInline(
    TranslationStackedInline,
):
    model = Section
    extra = 0


@admin.register(Page)
class PageAdmin(
    TranslationAdmin,
):
    save_on_top = True
    list_display = [
        "__str__",
        "path",
    ]
    search_fields = [
        "title",
        "path",
    ]
    inlines = [
        SectionAdminInline,
    ]
