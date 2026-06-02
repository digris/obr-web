import datetime
import pathlib

from django.core.management.base import BaseCommand

from stats import export


def parse_date(s):
    return datetime.date.fromisoformat(s)


class Command(BaseCommand):
    help = "Export stream events to Icecast log format"

    def add_arguments(self, parser):
        parser.add_argument(
            "--date-from",
            type=parse_date,
            required=True,
            help="YYYY-MM-DD",
        )
        parser.add_argument(
            "--date-until",
            type=parse_date,
            required=False,
            default=datetime.date.today(),
            help="YYYY-MM-DD ( defaults to today )",
        )
        parser.add_argument(
            "--dst-dir",
            type=pathlib.Path,
            required=True,
            help="log output directory",
        )
        parser.add_argument(
            "--database",
            type=str,
            default="default",
        )

    def handle(self, *args, **options):

        self.stdout.style_func = lambda x: x
        self.stderr.style_func = lambda x: x

        date_from = options["date_from"]
        date_until = options["date_until"]
        dst_dir = options["dst_dir"]
        database = options["database"]

        sessions_exported = export.sessions_export(
            date_from=date_from,
            date_until=date_until,
            dst_dir=dst_dir,
            database=database,
        )

        self.stderr.write("-" * 72)
        self.stderr.write(f"sessions exported: {sessions_exported}")
        self.stderr.write("-" * 72)
