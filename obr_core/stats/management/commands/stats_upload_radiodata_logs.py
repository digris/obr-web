import datetime

from django.core.management.base import BaseCommand

from stats import export


class Command(BaseCommand):
    help = "Upload logs to radio-data.ch FTP"

    def add_arguments(self, parser):
        parser.add_argument(
            "--num-days",
            type=int,
            default=1,
        )
        parser.add_argument(
            "--database",
            type=str,
            default="default",
        )

    def handle(self, *args, **options):

        self.stdout.style_func = lambda x: x
        self.stderr.style_func = lambda x: x

        num_days = options["num_days"]
        database = options["database"]

        today = datetime.date.today()
        date_until = today - datetime.timedelta(days=1)
        date_from = date_until - datetime.timedelta(days=num_days - 1)

        try:
            files_uploaded = export.radiodata_log_upload(
                date_from=date_from,
                date_until=date_until,
                database=database,
            )
        except export.ExporterError as e:
            self.stderr.write(f"error uploading logs: {str(e)}")
            return

        self.stderr.write("-" * 72)
        self.stderr.write(f"uploaded {len(files_uploaded)} files to FTP server")
