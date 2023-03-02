import argparse
import csv
import sys

from django.core.management.base import BaseCommand, CommandError

from catalog.models import Master
from google.cloud import storage
from progress.bar import Bar

# https://console.cloud.google.com/storage/browser?project=open-broadcast&prefix=
MASTER_BUCKET = "obr-master"
MEDIA_BUCKET = "obr-media"


class ValidationException(Exception):
    pass


def write_csv(outfile, data):
    assert len(data) > 0

    fieldnames = data[0].keys()
    writer = csv.DictWriter(
        outfile,
        fieldnames=fieldnames,
    )
    writer.writeheader()
    for row in data:
        writer.writerow(row)


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
        parser.add_argument(
            "-o",
            "--outfile",
            dest="outfile",
            type=argparse.FileType("w"),
            help="output result as csv",
        )

    def check_file_exists(self, bucket, path):
        if not path:
            print("PATH EMPTY!")
            return False
        try:
            return storage.Blob(bucket=bucket, name=path).exists(self.client)
        except ValueError as e:
            raise ValidationException(f"unable to verify {path}") from e

    def verify_master(self, master):
        uid = master.uid

        master_path = master.path
        dash_path = f"encoded/{uid}/dash/manifest.mpd"
        hls_path = f"encoded/{uid}/hls/manifest.m3u8"

        has_master = self.check_file_exists(self.master_bucket, master_path)
        has_dash = self.check_file_exists(self.media_bucket, dash_path)
        has_hls = self.check_file_exists(self.media_bucket, hls_path)

        return has_master, has_dash, has_hls

        # if not (has_master and has_dash and has_hls):
        #     self.stdout.write(
        #         f"{uid} - master: {has_master} - dash: {has_dash} - hls: {has_hls}"
        #     )

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

        tested = []

        for master in Bar(suffix="%(percent).1f%% - %(eta)ds").iter(qs):
            has_master, has_dash, has_hls = self.verify_master(master)
            tested.append(
                {
                    "uid": master.media.uid,
                    "has_master": has_master,
                    "has_dash": has_dash,
                    "has_hls": has_hls,
                }
            )

        # for master in qs:
        #     self.verify_master(master)

        # print(tested)

        problems = [
            t
            for t in tested
            if not (t["has_master"] and t["has_dash"] and t["has_hls"])
        ]

        if not problems:
            self.stdout.write(f"all {len(tested)} masters ok")
            sys.exit(0)

        if outfile := options["outfile"]:
            write_csv(outfile=outfile, data=problems)
