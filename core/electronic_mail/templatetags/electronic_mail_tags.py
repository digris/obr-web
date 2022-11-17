from django import template
from django.utils.html import mark_safe

register = template.Library()
styles = {
    # TODO: remove unused styles
    ".table": "font-size: inherit; width: 100%",
    ".center": "text-align: center",
    ".right": "text-align: right",
    ".link": "color: #0b87c9",
    ".dim": "color: #a0a0a0",
    ".cta": "color: red; height: 17px",
    ".button": "background: white",
    ".text-title": "color: #333333; line-height: 21px; font-size: 16px",
    ".text-xl": "font-size: 48px; line-height: 48px",
    ".text-semi-bold": "font-weight: 600",
    ".text-bold": "font-weight: 800",
    # layout elements
    ".table-container": "width: 100%;",
}


@register.simple_tag()
def style(names):
    inline_style = ";".join(styles.get(name, "") for name in names.split())
    return mark_safe(f'style="{inline_style}"')
