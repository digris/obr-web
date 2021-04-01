from django.core.management.base import BaseCommand, CommandError

from dev.schedule import synch_to_catalog

from catalog.models import Artist, Media


class Command(BaseCommand):
    help = "Sync schedule from (OBP API)"

    def handle(self, *args, **options):
        # Media.objects.all().delete()
        # Artist.objects.all().delete()
        synch_to_catalog()
