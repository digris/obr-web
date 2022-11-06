import requests
from django.http import HttpResponse


def ip(request):

    r = requests.get("https://curlmyip.org/")

    return HttpResponse(r.text)
