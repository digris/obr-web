from modeltranslation.translator import TranslationOptions, register

from .models import Newsletter


@register(Newsletter)
class NewsletterTranslationOptions(
    TranslationOptions,
):
    fields = [
        "title",
        "description",
    ]
