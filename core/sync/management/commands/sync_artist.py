from django.core.management.base import BaseCommand, CommandError
from catalog.models import Artist


class Command(BaseCommand):
    help = "Sync from OBP"

    def add_arguments(self, parser):
        parser.add_argument("artist_uids", nargs="+", type=str)

    def handle(self, *args, **options):
        for uid in options["artist_uids"]:
            try:
                artist = Artist.objects.get(uid=uid)
            except Artist.DoesNotExist:
                raise CommandError(f"artist does not exist: {uid}")

            # poll.opened = False
            # poll.save()

            artist.sync_data()

            self.stdout.write(f"sync completed for artist: {uid}")
