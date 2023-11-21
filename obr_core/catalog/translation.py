from modeltranslation.translator import TranslationOptions, register

from .models import Mood


@register(Mood)
class MoodTranslationOptions(TranslationOptions):
    fields = [
        "name",
        "teaser",
    ]
