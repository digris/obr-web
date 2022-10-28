from modeltranslation.translator import register, TranslationOptions
from .models import Category, Topic


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = [
        "name",
    ]


@register(Topic)
class TopicTranslationOptions(TranslationOptions):
    fields = [
        "question",
        "answer",
    ]
