from django.core.management.base import BaseCommand
from broadcast.models import Emission
from catalog.models import Playlist, Media, Release, Artist


class Command(BaseCommand):
    help = "Reset (= delete) synced data"

    def handle(self, *args, **options):

        models = [
            Emission,
            Playlist,
            Media,
            Release,
            Artist,
        ]

        for model in models:
            print(model.objects.all().delete())
