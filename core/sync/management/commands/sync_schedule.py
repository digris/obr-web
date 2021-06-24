import time
from datetime import datetime

from django.core.management.base import BaseCommand

from broadcast.sync import schedule


class Command(BaseCommand):
    help = "Sync schedule from OBP"

    def add_arguments(self, parser):
        parser.add_argument(
            "-s",
            "--date-start",
        )
        parser.add_argument(
            "-e",
            "--date-end",
        )
        parser.add_argument(
            "-f",
            "--force",
            action="store_true",
            default=False,
        )
        parser.add_argument(
            "-i",
            "--interval",
            type=int,
        )

    def sync_schedule(self, date_start, date_end, force):
        self.stdout.write(f"sync schedule: {date_start} - {date_end} - force: {force}")
        updated = list(
            schedule.sync_schedule(
                date_start=date_start,
                date_end=date_end,
                force=force,
            )
        )
        # TODO: find a better place to update airplays...
        # from catalog.sync.airplay import sync_airplays
        # from catalog.models.media import Airplay
        #
        # sync_airplays(time_start=Airplay.objects.latest().time_end)

        self.stdout.write(f"processed {len(updated)} emissions")

    def handle(self, *args, **options):
        date_start = options["date_start"]
        date_end = options["date_end"]
        force = options["force"]
        interval = options["interval"]

        date_start = datetime.strptime(date_start, "%Y-%m-%d") if date_start else None
        date_end = datetime.strptime(date_end, "%Y-%m-%d") if date_end else None

        if interval:
            while True:
                self.sync_schedule(date_start, date_end, force)
                self.stdout.write(f"rerun sync in {interval} seconds")
                time.sleep(interval)

        else:
            self.sync_schedule(date_start, date_end, force)
