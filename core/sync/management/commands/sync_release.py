from django.core.management.base import BaseCommand, CommandError
from catalog.models import Release


class Command(BaseCommand):
    help = "Sync from OBP"

    def add_arguments(self, parser):
        parser.add_argument("release_uids", nargs="+", type=str)

    def handle(self, *args, **options):
        for uid in options["release_uids"]:
            try:
                release = Release.objects.get(uid=uid)
            except Release.DoesNotExist:
                raise CommandError(f"release does not exist: {uid}")

            # poll.opened = False
            # poll.save()

            release.sync_data()

            self.stdout.write(f"sync completed for release: {uid}")
