from typing import Any

from rest_framework_simplejwt.serializers import (
    TokenObtainSlidingSerializer as BaseTokenObtainSlidingSerializer,
)
from rest_framework_simplejwt.serializers import (
    TokenRefreshSlidingSerializer as BaseTokenRefreshSlidingSerializer,
)
from rest_framework_simplejwt.settings import api_settings as simplejwt_settings

from .tokens import SlidingToken


class TokenObtainSlidingSerializer(BaseTokenObtainSlidingSerializer):
    token_class = SlidingToken
    pass


class TokenRefreshSlidingSerializer(BaseTokenRefreshSlidingSerializer):
    token_class = SlidingToken

    def validate(self, attrs: dict[str, Any]) -> dict[str, str]:
        # NOTE: we skip the default verification, as it does not take into account the
        #       "refresh_exp" claim
        #       https://github.com/jazzband/djangorestframework-simplejwt/issues/154
        token = self.token_class(attrs["token"], verify=False)

        # Check that the timestamp in the "refresh_exp" claim has not
        # passed
        token.check_exp(simplejwt_settings.SLIDING_TOKEN_REFRESH_EXP_CLAIM)

        # Update the "exp" and "iat" claims
        token.set_exp()
        token.set_iat()

        token.verify(claim=simplejwt_settings.SLIDING_TOKEN_REFRESH_EXP_CLAIM)

        return {"token": str(token)}
