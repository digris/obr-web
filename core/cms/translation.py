from modeltranslation.translator import register, TranslationOptions
from .models import Page, Section


@register(Page)
class CategoryTranslationOptions(
    TranslationOptions,
):
    fields = [
        "title",
        "lead",
    ]


@register(Section)
class TopicTranslationOptions(
    TranslationOptions,
):
    fields = [
        "title",
        "body",
    ]
