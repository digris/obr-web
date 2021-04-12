from django.core.management.base import BaseCommand, CommandError
from datetime import datetime
from sync import utils


class Command(BaseCommand):
    help = "Sync schedule from OBP"

    def add_arguments(self, parser):
        parser.add_argument(
            "-s",
            "--date-start",
        )

    def handle(self, *args, **options):
        date_start = options["date_start"]
        if date_start:
            date_start = datetime.strptime(date_start, "%Y-%m-%d")

        self.stdout.write(f"starting from date: {date_start}")
        updated = list(utils.sync_schedule(date_start=date_start))
        self.stdout.write(f"updated {len(updated)} emissions")
