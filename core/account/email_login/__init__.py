import logging
from django.conf import settings
from base.utils.signer import timestamp_signer
from django.core.signing import BadSignature, SignatureExpired

from electronic_mail.message import BaseMessage, SendMessageException

logger = logging.getLogger(__name__)


class SendLoginEmailException(Exception):
    pass


class SignedEmailValidationException(Exception):
    pass


def send_login_email(email):
    logger.info(f"send email login to {email}")
    signed_email = timestamp_signer.sign(str(email))
    print(signed_email)

    url = settings.SITE_URL + f"/account/email-login/{signed_email}/"

    from_email = "open broadcast radio <no-reply@openbroadcast.ch>"
    # to_email = "Peter Muster <ohrstrom@gmail.com>"
    to_email = email

    context = {
        "subject": "Your Account",
        "login_url": url,
    }
    template_dir = "account/email/login_email/"

    message = BaseMessage(
        from_email=from_email,
        to_email=to_email,
        template_dir=template_dir,
        context=context,
    )

    print(message.html)

    try:
        message.send()
    except SendMessageException as e:
        raise SendLoginEmailException(e)

    # print(url)


def validate_signed_email(signed_email, max_age=None):
    try:
        email = timestamp_signer.unsign(signed_email, max_age=max_age)
        return email
    except SignatureExpired:
        raise SignedEmailValidationException("Signature expired")
    except BadSignature:
        raise SignedEmailValidationException("Invalid signature")
