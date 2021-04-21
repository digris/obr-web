from django.core.management.base import BaseCommand

from dev.schedule import synch_to_catalog


class Command(BaseCommand):
    help = "Sync schedule from (OBP API)"

    def handle(self, *args, **options):
        # Media.objects.all().delete()
        # Artist.objects.all().delete()
        synch_to_catalog()
