import logging
import random
import string

from django.db.models.functions import Now

logger = logging.getLogger(__name__)


class TokenValidationError(Exception):
    pass


def generate_token(num_chars=6):
    # chars = string.ascii_uppercase + string.digits
    chars = string.ascii_uppercase
    return "".join(random.SystemRandom().choice(chars) for _ in range(num_chars))


def create_token_for_email(email):
    # pylint: disable=import-outside-toplevel
    from account.models import LoginToken

    token = LoginToken(email=email)
    token.save()
    return token


def claim_token(email, token):
    # pylint: disable=import-outside-toplevel
    from account.models import LoginToken

    value = token.upper().replace("-", "")
    logger.debug(f"validate: {value} - {email}")
    try:
        token = LoginToken.objects.get(email=email, value=value)
    except LoginToken.DoesNotExist as e:
        raise TokenValidationError("Invalid Token") from e

    if not token.is_valid:
        raise TokenValidationError("Expired Token")

    LoginToken.objects.filter(id=token.id).update(
        claimed=Now(),
    )

    return token.email


def delete_expired_tokens():
    # pylint: disable=import-outside-toplevel
    from account.models import LoginToken

    qs = LoginToken.objects.expired()
    qs.delete()
