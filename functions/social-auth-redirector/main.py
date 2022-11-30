import urllib.parse
from flask import render_template


BASE_URL = "https://next.openbroadcast.ch"


def auth_redirect(request):
    signed_email = request.args.get("signed_email", "")
    base_url = request.args.get("base_url", BASE_URL)
    email = signed_email.split(":")[0]
    quoted_signed_email = urllib.parse.quote(signed_email)
    login_url = f"{base_url}/account/email-login/{quoted_signed_email}/"
    return render_template("redirect.html", email=email, login_url=login_url)
