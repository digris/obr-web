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
            "--origin",
            type=str,
            choices=["icecast", "hls"],
            default=[],
            nargs="*",
            help="filter by origin ( includes all if not set )",
        )
        parser.add_argument(
            "--anonymize-ip",
            action="store_true",
            help="anonymize IP addresses ( 83.150.2.154 -> 83.150.2.0 )",
        )
        parser.add_argument(
            "--include-user",
            action="store_true",
            help="include device_key sha1 as user ( 83.150.2.154 - <user> - [... )",
        )
        parser.add_argument(
            "--dst-dir",
            type=pathlib.Path,
            required=True,
            help="log output directory",
        )
        parser.add_argument(
            "--filename-prefix",
            type=str,
            help="log filename prefix ( <prefix>-YYYY-MM-DD.icecast.log )",
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
        origin = options["origin"]
        dst_dir = options["dst_dir"]
        filename_prefix = options["filename_prefix"]
        anonymize_ip = options["anonymize_ip"]
        include_user = options["include_user"]
        database = options["database"]

        files_written = export.icecast_log_export(
            date_from=date_from,
            date_until=date_until,
            origin=origin,
            dst_dir=dst_dir,
            filename_prefix=filename_prefix,
            anonymize_ip=anonymize_ip,
            include_user=include_user,
            database=database,
        )

        self.stderr.write("-" * 72)
        self.stderr.write(f"files written: {len(files_written)}")
        self.stderr.write("-" * 72)

        num_lines_written = 0
        num_bytes_written = 0

        for path in files_written:
            num_bytes = path.stat().st_size

            with open(path, encoding="utf-8") as fp:
                num_lines = sum(1 for _ in fp)

            num_lines_written += num_lines
            num_bytes_written += num_bytes

            self.stderr.write(f"{str(path)}: {num_bytes} bytes, {num_lines} lines")

        self.stderr.write("-" * 72)
        self.stderr.write(
            f"total: {num_bytes_written} bytes, {num_lines_written} lines",
        )
        self.stderr.write("-" * 72)

        for path in files_written:
            self.stdout.write(path.resolve().as_posix())
