from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse

from .message import BaseMessage


@staff_member_required
def email_preview(request):

    context = {
        "subject": "foo the subject...",
    }
    from_email = "open broadcast radio <no-reply@openbroadcast.ch>"
    to_email = "Peter Muster <ohrstrom@gmail.com>"
    template_dir = "electronic_mail/default/"

    message = BaseMessage(
        from_email=from_email,
        to_email=to_email,
        template_dir=template_dir,
        context=context,
    )

    # message.send()

    if request.GET.get("plain"):
        text = "Subject: %s\n\n%s" % (message.subject, message.plain)
        return HttpResponse(text, content_type="text/plain")
    else:
        return HttpResponse(message.html)
