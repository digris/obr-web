import json

from django import template
from django.utils.html import mark_safe

from ..resizer import get_image_set

register = template.Library()


def parse_ratio(ratio_str):
    (
        a,
        b,
    ) = ratio_str.split(":")
    return int(a) / int(b)


@register.simple_tag
def src_set_as_json(image, kind=None, ratio=None):

    if not (image and image.file):
        return []

    # ratio is in format "16:9" as it is not (easily) possible to pass fractions from templates
    # templates, e.g. ratio=16/9

    # ugly...
    if not ratio and kind and ":" in kind:
        ratio = kind
        kind = None

    if ratio:
        ratio = parse_ratio(ratio)

    image_set = list(get_image_set(image.file, ratio=ratio, kind=kind))

    return mark_safe(json.dumps(image_set, indent=2))
