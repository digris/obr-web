from modeltranslation.translator import register, TranslationOptions
from .models import Mood


@register(Mood)
class MoodTranslationOptions(TranslationOptions):
    fields = [
        "name",
        "teaser",
    ]
