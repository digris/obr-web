import json

from django import template
from django.utils.html import mark_safe

register = template.Library()


@register.simple_tag()
def json_settings_as(settings):
    return mark_safe(json.dumps(settings))


@register.simple_tag
def json_settings(settings):
    return mark_safe(json.dumps(settings))
