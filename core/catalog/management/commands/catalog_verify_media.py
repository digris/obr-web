from django.core.management.base import BaseCommand, CommandError

from catalog.models import Master
from google.cloud import storage

# https://console.cloud.google.com/storage/browser?project=open-broadcast&prefix=
MASTER_BUCKET = "obr-master"
MEDIA_BUCKET = "obr-media"


class Command(BaseCommand):
    help = "Verify master files (and encoded versions)"

    client = storage.Client()
    master_bucket = client.bucket(MASTER_BUCKET)
    media_bucket = client.bucket(MEDIA_BUCKET)

    def add_arguments(self, parser):
        parser.add_argument(
            "media_uids",
            nargs="*",
            type=str,
        )
        parser.add_argument(
            "--database",
            type=str,
            default="default",
        )

    def check_file_exists(self, bucket, path):
        return storage.Blob(bucket=bucket, name=path).exists(self.client)

    def verify_master(self, master):
        uid = master.uid

        master_path = master.path
        dash_path = f"encoded/{uid}/dash/manifest.mpd"
        hls_path = f"encoded/{uid}/hls/manifest.m3u8"

        has_master = self.check_file_exists(self.master_bucket, master_path)
        has_dash = self.check_file_exists(self.media_bucket, dash_path)
        has_hls = self.check_file_exists(self.media_bucket, hls_path)

        if not (has_master and has_dash and has_hls):
            self.stdout.write(
                f"{uid} - master: {has_master} - dash: {has_dash} - hls: {has_hls}"
            )

    def handle(self, *args, **options):

        qs = (
            Master.objects.using(options["database"])
            .select_related(
                "media",
            )
            .all()
        )

        if media_uids := options["media_uids"]:
            qs = qs.filter(media__uid__in=media_uids)
            if qs.count() < 1:
                raise CommandError(f"no masters for uid: {', '.join(media_uids)}")

        self.stdout.write(f"num. masters to verify: {qs.count()}")

        for master in qs:
            self.verify_master(master)
