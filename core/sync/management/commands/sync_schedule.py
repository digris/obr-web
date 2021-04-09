from django.core.management.base import BaseCommand
from datetime import datetime

from sync import utils


class Command(BaseCommand):
    help = "Sync schedule from OBP"

    def add_arguments(self, parser):
        parser.add_argument(
            "-s",
            "--date-start",
            type=str,
            required=False,
        )

    def handle(self, *args, **options):
        date_start = options["date_start"]
        if date_start:
            date_start = datetime.strptime(date_start, "%Y-%m-%d")
        utils.sync_schedule(date_start=date_start)
