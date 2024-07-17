import jwt
from jwt.exceptions import InvalidAlgorithmError, InvalidTokenError
from rest_framework_simplejwt.settings import api_settings as simplejwt_settings
from rest_framework_simplejwt.tokens import BlacklistMixin
from rest_framework_simplejwt.tokens import Token as BaseToken
from rest_framework_simplejwt.tokens import TokenBackendError, TokenError


class Token(BaseToken):
    pass


class SlidingToken(BlacklistMixin, Token):
    token_type = "sliding"  # noqa S105
    lifetime = simplejwt_settings.SLIDING_TOKEN_LIFETIME

    def __init__(self, token=None, verify=True, *args, **kwargs) -> None:
        super().__init__(token, verify, *args, **kwargs)

        if self.token is None:
            # Set sliding refresh expiration claim if new token
            self.set_exp(
                simplejwt_settings.SLIDING_TOKEN_REFRESH_EXP_CLAIM,
                from_time=self.current_time,
                lifetime=simplejwt_settings.SLIDING_TOKEN_REFRESH_LIFETIME,
            )

        elif token and not verify:
            # NOTE: in case verification is skipped in init, we need to run it here
            self.decode(token)

    def decode(self, token) -> dict:
        token_backend = self.get_token_backend()
        try:
            return jwt.decode(
                token,
                token_backend.get_verifying_key(token),
                algorithms=[token_backend.algorithm],
                audience=token_backend.audience,
                issuer=token_backend.issuer,
                leeway=token_backend.get_leeway(),
                options={
                    "verify_aud": token_backend.audience is not None,
                    "verify_signature": True,
                    # NOTE: this is the only change from the default backend decode
                    #       we do not want to verify "exp" - we verify "refresh_exp" instead
                    "verify_exp": False,
                },
            )
        except InvalidAlgorithmError as e:
            raise TokenBackendError("Invalid algorithm specified") from e
        except InvalidTokenError as e:
            raise TokenBackendError("Token is invalid or expired") from e

    def verify(self, claim: str = "exp") -> None:
        # NOTE: we override the default verification, to allow optionally
        #       checking the "refresh_exp" claim in the refresh-flow
        #       https://github.com/jazzband/djangorestframework-simplejwt/issues/154
        self.check_exp(claim=claim)

        if (
            simplejwt_settings.JTI_CLAIM is not None
            and simplejwt_settings.JTI_CLAIM not in self.payload
        ):
            raise TokenError("Token has no id")

        if simplejwt_settings.TOKEN_TYPE_CLAIM is not None:
            self.verify_token_type()
