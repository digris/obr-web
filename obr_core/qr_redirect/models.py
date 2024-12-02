import base64
import io

from django.conf import settings
from django.db import models
from django.urls import reverse

import qrcode
from common.models.mixins import CTUIDModelMixin, TimestampedModelMixin
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import GappedSquareModuleDrawer

SITE_URL = getattr(settings, "SITE_URL", "")


class QRRedirect(
    CTUIDModelMixin,
    TimestampedModelMixin,
    models.Model,
):
    target_url = models.URLField(
        max_length=512,
        verbose_name="Target URL",
    )

    name = models.CharField(
        max_length=64,
        verbose_name="Name",
        blank=True,
        default="",
    )

    num_clicks = models.PositiveIntegerField(
        verbose_name="Number of Clicks",
        default=0,
    )

    class Meta:
        app_label = "qr_redirect"
        verbose_name = "QR-Code"
        verbose_name_plural = "QR-Codes"
        ordering = [
            "target_url",
        ]

    def __str__(self):
        return self.target_url

    @property
    def qr_code_url(self):
        relative_url = reverse(
            "qr-redirect:redirect",
            kwargs={
                "uid": str(self.uid),
            },
        )
        return f"{SITE_URL}{relative_url}"

    @property
    def qr_code(self):
        qr = qrcode.QRCode(
            version=4,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=50,
            border=0,
        )
        qr.add_data(self.qr_code_url)
        qr.make(fit=True)

        img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=GappedSquareModuleDrawer(
                size_ratio=0.8,
            ),
        )

        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        return buffer

    @property
    def qr_code_base64(self):
        img_base64 = base64.b64encode(self.qr_code.getvalue()).decode("utf-8")

        return f"data:image/png;base64,{img_base64}"
