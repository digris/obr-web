from modeltranslation.translator import TranslationOptions, register

from .models import Editor


@register(Editor)
class EditorTranslationOptions(TranslationOptions):
    fields = [
        "description",
    ]
