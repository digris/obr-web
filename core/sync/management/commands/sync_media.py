from django.core.management.base import BaseCommand, CommandError

from catalog.models import Media


class Command(BaseCommand):
    help = "Sync from OBP"

    def add_arguments(self, parser):
        parser.add_argument("media_uids", nargs="+", type=str)

    def handle(self, *args, **options):
        for uid in options["media_uids"]:
            try:
                media = Media.objects.get(uid=uid)
            except Media.DoesNotExist:
                raise CommandError(f"media does not exist: {uid}")

            # poll.opened = False
            # poll.save()

            media.sync_data()

            self.stdout.write(f"sync completed for media: {uid}")
