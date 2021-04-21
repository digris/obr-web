from django.http import HttpResponseRedirect
from django.views.generic import View

DASH_MANIFEST_URL_TPL = "https://media.next.openbroadcast.ch/encoded/{uid}/manifest.mpd"


class MediaManifestRedirectView(View):
    def get(self, request, uid, *args, **kwargs):
        # uid = kwargs.get('uid')
        url = DASH_MANIFEST_URL_TPL.format(uid=uid)

        response = HttpResponseRedirect(redirect_to=url)
        # response = HttpResponse('blup')
        # response['Access-Control-Allow-Origin'] = '*'
        response["Access-Control-Allow-Origin"] = "http://next.openbroadcast.ch:3000"
        response["Access-Control-Allow-Credentials"] = "true"

        cookie_value = "URLPrefix=aHR0cDovL21lZGlhLm9ici1uZXh0LmhhemVsZmlyZS5jb20vZW5jb2RlZA==:Expires=1616491154:KeyName=cdn-key:Signature=C7aVC2hiQ_zNX_zNG7NftlksBn0="
        cookie_str = f"Cloud-CDN-Cookie={cookie_value}; Path=/; Domain=next.openbroadcast.ch; HttpOnly: SameSite=Lax"

        # response['Set-Cookie'] = cookie_str

        return response
