from modeltranslation.translator import register, TranslationOptions
from .models import Newsletter


@register(Newsletter)
class NewsletterTranslationOptions(
    TranslationOptions,
):
    fields = [
        "title",
        "description",
    ]
