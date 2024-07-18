#!/usr/bin/env python3
import re
import pytz
import http.cookies
import datetime

"""
curl --cookie "Cloud-CDN-Cookie=URLPrefix=aHR0cHM6Ly9tZWRpYS5vcGVuYnJvYWRjYXN0LmNoL2VuY29kZWQ=:Expires=1721308780:KeyName=cdn-key:Signature=YZ1MOde2rsKV-sucFvddUBTCDKs=" http://localhost:8008/
"""

TIMEZONE = pytz.timezone("Europe/Zurich")

def app(environ, start_response):
    cookie_string = environ.get('HTTP_COOKIE', '')
    cookies = http.cookies.SimpleCookie(cookie_string)
    cloud_cdn_cookie = cookies.get('Cloud-CDN-Cookie', None)

    is_valid = True

    status = '200 OK'
    response = 'Valid'

    if cloud_cdn_cookie:
        match = re.search(r'Expires=(\d+)', cloud_cdn_cookie.value)
        if match:
            now = datetime.datetime.now(pytz.utc).astimezone(TIMEZONE).replace(tzinfo=pytz.utc)
            expires_at = datetime.datetime.fromtimestamp(int(match.group(1)), pytz.utc)
            # print("now:     ", now)
            # print("expires: ", expires_at)
            print("expires in:", (expires_at - now).total_seconds())
            if expires_at < now:
                is_valid = False
        else:
            is_valid = False

    status = '200 OK' if is_valid else '403 Forbidden'
    response = 'OK' if is_valid else 'Invalid CDN Cookie'

    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    return [response.encode()]
