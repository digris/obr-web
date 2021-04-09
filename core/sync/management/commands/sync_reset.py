from django.core.management.base import BaseCommand
from broadcast.models import Emission
from catalog.models import Playlist


class Command(BaseCommand):
    help = "Reset (= delete) synced data"

    def handle(self, *args, **options):

        models = [
            Emission,
            Playlist,
        ]

        for model in models:
            print(model.objects.all().delete())
