from django.contrib import admin
from django.utils.html import mark_safe

from .models import QRRedirect


@admin.register(QRRedirect)
class QRRedirectAdmin(
    admin.ModelAdmin,
):
    save_on_top = True
    list_display = [
        "target_url",
        "name",
        "num_clicks",
        "uid",
        "qr_code_display",
    ]
    search_fields = [
        "target_url",
        "name",
    ]

    @admin.display(
        description="QR-Code",
    )
    def qr_code_display(self, obj):
        return mark_safe(
            """
            <img src="{}" style="max-width: 200px; max-height: 200px;">
            """.format(
                obj.qr_code_base64,
            ),
        )
