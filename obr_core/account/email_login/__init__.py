import logging
import urllib.parse

from django.conf import settings
from django.core.signing import BadSignature, SignatureExpired
from django.utils.translation import gettext_lazy as _

from account import token_login
from common.utils.signer import timestamp_signer
from electronic_mail.message import BaseMessage, SendMessageError

logger = logging.getLogger(__name__)


class SendLoginEmailError(Exception):
    pass


class SignedEmailValidationError(Exception):
    pass


def send_login_email(email):
    logger.info(f"send email login to {email}")
    signed_email = timestamp_signer.sign(str(email))
    quoted_signed_email = urllib.parse.quote(signed_email)

    # NOTE: improve token handling...
    login_token = token_login.create_token_for_email(email=email)

    login_url = settings.SITE_URL + f"/account/email-login/{quoted_signed_email}/"

    from_email = "open broadcast radio <no-reply@openbroadcast.ch>"
    to_email = email

    context = {
        "subject": f"Login Code: {login_token}",
        "title": "Code",
        "login_url": login_url,
        "login_token": login_token,
    }
    template_dir = "account/email/login_email/"

    message = BaseMessage(
        from_email=from_email,
        to_email=to_email,
        template_dir=template_dir,
        context=context,
    )

    try:
        message.send()
    except SendMessageError as e:
        raise SendLoginEmailError(e) from e


def validate_signed_email(signed_email, max_age=None):
    try:
        email = timestamp_signer.unsign(signed_email, max_age=max_age)
        return email
    except SignatureExpired as e:
        raise SignedEmailValidationError(_("Signature expired")) from e
    except BadSignature as e:
        raise SignedEmailValidationError(_("Invalid signature")) from e
