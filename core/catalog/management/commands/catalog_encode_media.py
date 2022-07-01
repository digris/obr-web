import urllib3
import certifi
import json
from django.core.management.base import BaseCommand, CommandError
from catalog.models import Master

ENCODER_ENDPOINT = "https://media-encoder-kcek2ea7xq-oa.a.run.app"


class Command(BaseCommand):
    help = "(Re-)Encode media to DASH & HLS"
    api_token = ""

    def add_arguments(self, parser):
        parser.add_argument(
            "media_uids",
            nargs="+",
            type=str,
        )
        parser.add_argument(
            "--token",
            type=str,
            help="CF API token",
            required=True,
        )
        parser.add_argument(
            "--database",
            type=str,
            default="default",
        )

    def encode_format(self, path, encoding_format):
        print(f"encode: {path} to {encoding_format}")
        payload = {"path": path}
        url = f"{ENCODER_ENDPOINT}/encode-{encoding_format}"
        headers = {
            "Content-Type": "application/json",
            "Authentication": f"Bearer {self.api_token}",  # Note: Flask style authentication header
        }
        body = json.dumps(payload).encode("utf-8")
        http = urllib3.PoolManager(ca_certs=certifi.where())
        r = http.request("POST", url=url, body=body, headers=headers)
        return json.loads(r.data.decode("utf-8"))

    def encode_master(self, master):
        self.stdout.write(f"encode uid: {master.path}\n")
        dash = self.encode_format(master.path, "dash")
        self.stdout.write(f"dash: {dash}\n")
        hls = self.encode_format(master.path, "hls")
        self.stdout.write(f"hls: {hls}\n")

    def handle(self, *args, **options):

        self.api_token = options["token"]

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
                raise CommandError(f"no media for uid: {', '.join(media_uids)}")

        self.stdout.write(f"num. media to encode: {qs.count()}")

        for master in qs:
            self.encode_master(master)