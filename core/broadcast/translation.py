from modeltranslation.translator import register, TranslationOptions
from .models import Editor


@register(Editor)
class EditorTranslationOptions(TranslationOptions):
    fields = [
        "description",
    ]
