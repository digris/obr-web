from django.core.management.base import BaseCommand, CommandError

from account.models import User


class Command(BaseCommand):
    help = "Sync from OBP"

    def add_arguments(self, parser):
        parser.add_argument("user_uids", nargs="+", type=str)

    def handle(self, *args, **options):
        for uid in options["user_uids"]:
            try:
                user = User.objects.get(uid=uid)
            except User.DoesNotExist:
                raise CommandError(f"user does not exist: {uid}")

            user.sync_data()

            self.stdout.write(f"sync completed for user: {uid}")
