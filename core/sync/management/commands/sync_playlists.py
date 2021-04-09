from django.core.management.base import BaseCommand

from sync import utils


class Command(BaseCommand):
    help = "Sync from OBP"

    def handle(self, *args, **options):
        utils.sync_playlists()
