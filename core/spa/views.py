from django.shortcuts import render
import urllib
from django.views.generic import TemplateView
from catalog.utils import get_signed_cookie


class SPAIndexView(TemplateView):
    template_name = "spa/index.html"
    path = ""

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        # path = kwargs.get("path", "")

        if request.user.is_authenticated:
            signed_cookie = get_signed_cookie()
            cookie_str = f"{signed_cookie}; Path=/; Domain=next.openbroadcast.ch; HttpOnly: SameSite=Lax"

            response["Set-Cookie"] = cookie_str
            # print("cookie_str", cookie_str)

        return response
