# -*- coding: utf-8 -*-
import os
from smtplib import SMTPException

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


class SendMessageException(Exception):
    pass


class BaseMessage:

    static_url = settings.STATIC_URL
    site_url = settings.SITE_URL

    # template_plain = "electronic_mail/messages/default.txt"
    # template_html = "electronic_mail/messages/default.html"

    def __init__(self, from_email, to_email, template_dir, context):

        self.template_plain = os.path.join(template_dir, "message.txt")
        self.template_html = os.path.join(template_dir, "message.html")

        context.update(
            {
                "STATIC_URL": self.static_url,
                "SITE_URL": self.site_url,
            }
        )
        self.from_email = from_email
        self.to_email = [to_email]

        self.subject = context.get("subject", "-")
        self.plain = render_to_string(self.template_plain, context)
        self.html = render_to_string(self.template_html, context)

    def send(self):
        mail = EmailMultiAlternatives(
            subject=self.subject,
            body=self.plain,
            from_email=self.from_email,
            to=self.to_email,
        )
        mail.attach_alternative(self.html, "text/html")
        try:
            return mail.send()
        except (SMTPException, ConnectionError) as e:
            raise SendMessageException(e)
