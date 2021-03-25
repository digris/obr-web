# -*- coding: utf-8 -*-
def get_absolute_url(request, url):
    return f"{request.scheme}://{request.get_host()}{url}"
