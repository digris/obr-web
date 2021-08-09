import logging
import random
import string

logger = logging.getLogger(__name__)


class TokenValidationException(Exception):
    pass


def generate_token(num_chars=6):
    chars = string.ascii_uppercase + string.digits
    return "".join(random.SystemRandom().choice(chars) for _ in range(num_chars))


def create_token_for_email(email):
    # pylint: disable=import-outside-toplevel
    from account.models import LoginToken

    token = LoginToken(email=email)
    token.save()
    return token


# pylint: disable=unused-argument
def validate_token(email, token, max_age=None):
    # pylint: disable=import-outside-toplevel
    from account.models import LoginToken

    value = token.upper().replace("-", "")
    logger.debug(f"validate: {value} - {email}")
    # TODO: implement `max_age`
    qs = LoginToken.objects.filter(email=email, value=value)
    if not qs.exists():
        raise TokenValidationException("Invalid Token")

    return qs.first().email
