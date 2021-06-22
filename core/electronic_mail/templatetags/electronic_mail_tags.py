from django import template
from django.utils.html import mark_safe

register = template.Library()
styles = {
    ".table": "font-size: inherit; width: 100%",
    ".total": "font-weight: bold",
    ".center": "text-align: center",
    ".right": "text-align: right",
    ".link": "color:  #0b87c9",
    ".dim": "color:  #a0a0a0",
    ".cta": "color: red; height: 17px",
    ".button": "background: white",
    ".login-token": "background: white; font-size: 48px;",
}


@register.simple_tag()
def style(names):

    inline_style = ";".join(styles.get(name, "") for name in names.split())
    return mark_safe(f'style="{inline_style}"')
