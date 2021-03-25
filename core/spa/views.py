from django.shortcuts import render
import urllib
from django.views.generic import TemplateView
from catalog.utils import get_signed_cookie


class SPAIndexView(TemplateView):
    template_name = "spa/index.html"
    path = ""

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        path = kwargs.get("path", "")
        print("path", path)
        # set_cookie(key, value='', max_age=None, expires=None, path='/', domain=None, secure=None, httponly=False, samesite=None) :

        signed_cookie = get_signed_cookie()

        cookie_str = f"{signed_cookie}; Path=/; Domain=next.openbroadcast.ch; HttpOnly: SameSite=Lax"

        # cookie_value = 'URLPrefix=aHR0cDovL21lZGlhLm9ici1uZXh0LmhhemVsZmlyZS5jb20vZW5jb2RlZA==:Expires=1616493753:KeyName=cdn-key:Signature=rXDH0NGBSIrqnO1RHmR9oiFhfpc='
        # cookie_str = f'Cloud-CDN-Cookie={cookie_value}; Path=/; Domain=next.openbroadcast.ch; HttpOnly: SameSite=Lax'

        response["Set-Cookie"] = cookie_str

        print(cookie_str)

        # response.set_cookie(
        #     "Cloud-CDN-Cookie",
        #     value=str(cookie_value),
        #     domain="next.openbroadcast.ch",
        #     path="/",
        #     httponly=True,
        #     samesite="Lax",
        # )
        #

        # response.set_cookie(
        #     "CDN-FOO",
        #     value="BAR",
        #     path="/",
        #     httponly=True,
        # )
        print("*****")
        return response
