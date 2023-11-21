from django.core.management.base import BaseCommand, CommandError

from broadcast.models import Editor


class Command(BaseCommand):
    help = "Sync from OBP"

    def add_arguments(self, parser):
        parser.add_argument("editor_uids", nargs="+", type=str)

    def handle(self, *args, **options):
        for uid in options["editor_uids"]:
            try:
                editor = Editor.objects.get(uid=uid)
            except Editor.DoesNotExist:
                raise CommandError(f"editor does not exist: {uid}")

            editor.sync_data()

            self.stdout.write(f"sync completed for editor: {uid}")
