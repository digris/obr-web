from django.core.management.base import BaseCommand, CommandError

from catalog.models import Playlist


class Command(BaseCommand):
    help = "Sync from OBP"

    def add_arguments(self, parser):
        parser.add_argument("playlist_uids", nargs="+", type=str)

    def handle(self, *args, **options):
        for uid in options["playlist_uids"]:
            try:
                playlist = Playlist.objects.get(uid=uid)
            except Playlist.DoesNotExist:
                raise CommandError(f"playlist does not exist: {uid}")

            playlist.sync_data()

            self.stdout.write(f"sync completed for playlist: {uid}")
