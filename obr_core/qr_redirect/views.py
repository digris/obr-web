import logging

from django.db.models import F
from django.shortcuts import redirect

from .models import QRRedirect

logger = logging.getLogger(__name__)


def qr_redirect_view(request, uid):
    try:
        code = QRRedirect.objects.get(uid=uid)
    except QRRedirect.DoesNotExist:
        logger.warning(f"QR-Redirect with UID {uid} not found.")
        return redirect("/")

    logger.debug(f"Redirecting {uid} to {code.target_url}")

    # increase num_clicks
    QRRedirect.objects.filter(uid=uid).update(num_clicks=F("num_clicks") + 1)

    return redirect(code.target_url, permanent=False)
