from modeltranslation.translator import TranslationOptions, register

from .models import Page, Section


@register(Page)
class PageTranslationOptions(
    TranslationOptions,
):
    fields = [
        "title",
        "lead",
    ]


@register(Section)
class SectionTranslationOptions(
    TranslationOptions,
):
    fields = [
        "title",
        "body",
        "cta_title",
        "cta_url",
    ]
