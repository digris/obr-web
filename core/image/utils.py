from django.utils.safestring import mark_safe
from .resizer import get_resized_url


def get_admin_inline_image(obj, width=80, height=80):
    if obj.image and obj.image.file:
        url = get_resized_url(obj.image.file, width, height, "crop")
        html = f'<img loading="lazy" width="{width}" height="{height}" src="{url}" />'
    else:
        html = f'<div style="width: {width}px; height: {height}px; background: rgba(128,128,128,0.2)"></div>'

    return mark_safe(html)
