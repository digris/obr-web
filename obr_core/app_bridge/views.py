import urllib.parse

from django.http import HttpResponseForbidden, HttpResponseRedirect

from common.utils.signer import timestamp_signer

REDIRECTOR_URL = (
    "https://europe-west6-open-broadcast.cloudfunctions.net/social-auth-redirector"
)


def social_auth_redirect(request):
    if request.user and request.user.is_authenticated:
        signed_email = timestamp_signer.sign(str(request.user.email))
        quoted_signed_email = urllib.parse.quote(signed_email)
        base_url = f"{request.scheme}://{request.get_host()}"
        url = f"{REDIRECTOR_URL}?signed_email={quoted_signed_email}&base_url={base_url}"
        return HttpResponseRedirect(url)

    return HttpResponseForbidden()
