from django.apps import apps
from django.http import HttpResponseRedirect
from rest_framework.views import APIView

OBP_URL = "https://www.openbroadcast.org"
OBP_URL_MAP = {
    "catalog.artist": "content/library/artists",
}


class OBPRedirectView(APIView):
    @staticmethod
    def get_redirect_url(ct, uuid):
        path = OBP_URL_MAP.get(ct)
        return f"{OBP_URL}/{path}/{uuid}/"

    def get(self, request, obj_ct, obj_uid):
        content_object = apps.get_model(*obj_ct.split(".")).objects.get(uid=obj_uid)
        redirect_url = self.get_redirect_url(content_object.ct, content_object.uuid)
        return HttpResponseRedirect(redirect_url)
