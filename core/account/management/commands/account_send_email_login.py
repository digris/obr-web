from django.core.management.base import BaseCommand, CommandError
from django.core.validators import validate_email

from account import email_login


class Command(BaseCommand):
    help = "Send login token to e-mail address"

    def add_arguments(self, parser):
        parser.add_argument(
            "--email",
            dest="email",
            type=str,
            # action=validate_email,
            required=True,
        )

    def handle(self, *args, **options):
        email = options["email"]

        validate_email(email)

        email_login.send_login_email(email=email)
