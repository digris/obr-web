from django.http import HttpResponse, HttpResponsePermanentRedirect

from electronic_mail.message import BaseMessage


def email_login_code(request):
    from_email = "open broadcast radio <no-reply@openbroadcast.ch>"
    to_email = "Jonas Ohrstrom <ohrstrom@gmail.com>"
    login_token = "AAA-XXX"
    login_url = "http://example.com"

    context = {
        "subject": f"Login Code: {login_token}",
        "title": "Login Code",
        "login_url": login_url,
        "login_token": login_token,
    }
    template_dir = "account/email/login_email/"

    message = BaseMessage(
        from_email=from_email,
        to_email=to_email,
        template_dir=template_dir,
        context=context,
    )

    if request.GET.get("plain"):
        text = f"Subject: {message.subject}\n\n{message.plain}"
        return HttpResponse(
            text,
            content_type="text/plain",
            charset="utf-8",
        )

    return HttpResponse(message.html)


def redirect(request):
    return HttpResponsePermanentRedirect(
        "https://next.openbroadcast.ch/proto/app-bridge/"
    )
