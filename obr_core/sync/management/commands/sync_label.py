from django.core.management.base import BaseCommand, CommandError

from catalog.models import Label


class Command(BaseCommand):
    help = "Sync from OBP"

    def add_arguments(self, parser):
        parser.add_argument("label_uids", nargs="+", type=str)

    def handle(self, *args, **options):
        for uid in options["label_uids"]:
            try:
                label = Label.objects.get(uid=uid)
            except Label.DoesNotExist:
                raise CommandError(f"label does not exist: {uid}")

            label.sync_data(skip_media=False)

            self.stdout.write(f"sync completed for label: {uid}")
