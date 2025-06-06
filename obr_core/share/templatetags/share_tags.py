from django import template

from ..meta import get_image_preload_for_request, get_meta_for_request

register = template.Library()


@register.inclusion_tag(
    "share/templatetags/_meta.html",
    takes_context=True,
)
def opengraph_meta(context):
    if request := context.get("request"):
        return {
            "meta": get_meta_for_request(request),
        }
    return {}


@register.inclusion_tag(
    "share/templatetags/_image-preload.html",
    takes_context=True,
)
def image_preload(context):
    if request := context.get("request"):
        return {
            "url": get_image_preload_for_request(request),
        }
    return {}
