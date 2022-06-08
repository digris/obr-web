from modeltranslation.translator import register, TranslationOptions
from .models import Mood


@register(Mood)
class NewsTranslationOptions(TranslationOptions):
    fields = [
        "name",
        "teaser",
    ]
