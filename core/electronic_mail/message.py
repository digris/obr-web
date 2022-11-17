import logging
import os
from smtplib import SMTPException
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, SendGridException

SENDGRID_API_KEY = getattr(settings, "SENDGRID_API_KEY", None)

logger = logging.getLogger(__name__)


class SendMessageException(Exception):
    pass


class BaseMessage:

    static_url = settings.STATIC_URL
    site_url = settings.SITE_URL

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
        self.html = render_to_string(self.template_html, context)
        self.plain = render_to_string(self.template_plain, context)

    def send(self):
        if SENDGRID_API_KEY and not getattr(settings, "TEST_MODE", False):
            sg = SendGridAPIClient(SENDGRID_API_KEY)
            message = Mail(
                from_email=self.from_email,
                to_emails=self.to_email,
                subject=self.subject,
                html_content=self.html,
                plain_text_content=self.plain,
            )
            try:
                response = sg.send(message)
                logger.debug(
                    f"sent message to {self.to_email} - status code: {response.status_code}"
                )
                return response
            except SendGridException as e:
                raise SendMessageException(e) from e
        else:
            # for e2e tests we need "local" delivery
            logger.info("SENDGRID_API_KEY not configured")
            mail = EmailMessage(
                subject=self.subject,
                body=self.plain,
                from_email=self.from_email,
                to=self.to_email,
            )
            try:
                return mail.send()
            except (SMTPException, ConnectionError) as e:
                raise SendMessageException(e) from e
