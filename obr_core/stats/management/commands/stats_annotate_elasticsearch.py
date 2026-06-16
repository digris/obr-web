import json
import sqlite3
import elasticsearch
import elasticsearch.helpers
import time
from ipaddress import ip_address, ip_network

from django.core.management.base import BaseCommand
from django.conf import settings

from ipwhois import IPWhois


ES_API_URL = settings.STATS_ES_API_URL
ES_API_KEY = settings.STATS_ES_API_KEY

WHOIS_CACHE = settings.PROJECT_ROOT / "data" / "whois" / "whois.db"

class CachedWhois:
    def __init__(self):
        self._nets = []  # list[(IPv4Network, data)]
        self.whois_cache = WHOIS_CACHE  # e.g. "data/whois.db"

        self._db = sqlite3.connect(self.whois_cache)
        self._db.execute("""
            CREATE TABLE IF NOT EXISTS whois_cache (
                cidr TEXT PRIMARY KEY,
                data TEXT NOT NULL
            )
        """)
        self._db.commit()

        self._load_cache()

    def _load_cache(self):
        for cidr, data in self._db.execute("SELECT cidr, data FROM whois_cache"):
            self._nets.append((ip_network(cidr), json.loads(data)))

    @staticmethod
    def extract_network_descr(result):
        network = result.get("network") or {}
        remarks = network.get("remarks") or []

        for remark in remarks:
            desc = remark.get("description")
            if not desc:
                continue
            if isinstance(desc, list):
                return desc[0]
            if isinstance(desc, str):
                return desc
        return None

    # @staticmethod
    # def extract_org_name(result):
    #     for obj in result.get("objects", {}).values():
    #         contact = obj.get("contact", {})
    #         if contact.get("kind") == "org":
    #             return contact.get("name")
    #     return None
    

    @classmethod
    def extract_org_name(cls, result):
        # 1) Real RDAP org object
        for obj in result.get("objects", {}).values():
            contact = obj.get("contact") or {}
            if contact.get("kind") == "org" and contact.get("name"):
                return contact["name"]

        # 2) Registrant role/group/individual
        for obj in result.get("objects", {}).values():
            roles = obj.get("roles") or []
            contact = obj.get("contact") or {}

            if "registrant" in roles and contact.get("name"):
                name = contact["name"]

                # skip maintainer handles like BLUEWINNET-MNT
                if not name.endswith("-MNT"):
                    return name

        # 3) Contact address often contains company name
        for obj in result.get("objects", {}).values():
            contact = obj.get("contact") or {}
            addresses = contact.get("address") or []

            for address in addresses:
                value = address.get("value") or ""
                first_line = value.splitlines()[0].strip()

                if first_line:
                    return first_line

        # 4) ASN description fallback
        return cls.clean_org_name(result.get("asn_description"))

    @staticmethod
    def extract_owner(result):
        for obj in result.get("objects", {}).values():
            contact = obj.get("contact", {})
            if contact.get("kind") == "org":
                return contact.get("name")
        return result.get("asn_description")

    def _lookup_sqlite(self, ip_obj):
        # brute-force is fine: number of rows is small
        for cidr, data in self._db.execute("SELECT cidr, data FROM whois_cache"):
            net = ip_network(cidr)
            if ip_obj in net:
                parsed = json.loads(data)
                # promote to memory cache
                self._nets.append((net, parsed))
                return parsed
        return None

    def __call__(self, ip: str):
        ip_obj = ip_address(ip)

        # 1) in-memory cache hit
        for net, data in self._nets:
            if ip_obj in net:
                print(
                    f"Memory cache hit for IP {ip} - ASN {data['asn']} - {data['asn_cidr']} - {data['network_name']}  - {data['org_name']}"
                )
                return data

        # 2) sqlite cache hit (authoritative)
        data = self._lookup_sqlite(ip_obj)
        if data:
            print(
                f"SQLite cache hit for IP {ip} - ASN {data['asn']} - {data['asn_cidr']} - {data['network_name']}  - {data['org_name']}"
            )
            return data

        # 3) WHOIS lookup
        try:
            result = IPWhois(ip, timeout=2).lookup_rdap(depth=0, inc_nir=False)
        except Exception as e:
            print(e)
            return None

        cidr = result.get("asn_cidr")
        if not cidr or cidr == "NA":
            print(f"No usable ASN CIDR for IP {ip}: {cidr}")
            return None

        try:
            net = ip_network(cidr)
        except ValueError:
            print(f"Invalid ASN CIDR for IP {ip}: {cidr!r}")
            return None

        data = {
            "rir": result.get("asn_registry"),
            "asn": result.get("asn"),
            "asn_cidr": cidr,
            "asn_country_code": result.get("asn_country_code"),
            "asn_description": result.get("asn_description"),
            "network_name": result.get("network", {}).get("name"),
            # "network_descr": self.extract_network_descr(result),
            "owner": self.extract_owner(result),
            "org_name": self.extract_org_name(result),
        }

        # 3) update memory + persist
        self._nets.append((net, data))
        self._db.execute(
            "INSERT OR IGNORE INTO whois_cache (cidr, data) VALUES (?, ?)",
            (cidr, json.dumps(data)),
        )
        self._db.commit()

        print(f"WHOIS lookup for IP {ip} - ASN {data['asn']} - {data['asn_cidr']} - {data['network_name']}  - {data['org_name']}")
        time.sleep(0.5)  # be nice to the WHOIS

        return data


class EsService:
    client: elasticsearch.Elasticsearch
    index = "listener-sessions"

    def __init__(self):
        self.client = elasticsearch.Elasticsearch(
            ES_API_URL,
            api_key=ES_API_KEY,
            verify_certs=False,
            ssl_show_warn=False,
            request_timeout=10,
        )

    def iter_top_ips(self, size=1000):
        resp = self.client.search(
            index=self.index,
            size=0,
            aggs={
                "top_ips": {
                    "terms": {
                        "field": "remote_addr.keyword",
                        "size": size,
                        "order": {"_count": "desc"},
                    }
                }
            },
            query={
                "bool": {
                    "must": [
                        {
                            "range": {
                                "time_start": {
                                    "gte": "2025-01-01T00:00:00"
                                }
                            }
                        }
                    ],
                    "must_not": [
                        {
                            "exists": {
                                "field": "whois.rir"
                            }
                        }
                    ]
                }
            }
        )

        for b in resp["aggregations"]["top_ips"]["buckets"]:
            yield b["key"], b["doc_count"]

    def update_ip(self, ip, whois):
        self.client.update_by_query(
            index=self.index,
            conflicts="proceed",
            refresh=False,
            wait_for_completion=False,
            requests_per_second=500,
            query={
                "bool": {
                    "must": [{"term": {"remote_addr.keyword": ip}}],
                    "must_not": [{"exists": {"field": "whois.rir"}}],
                }
            },
            script={
                "source": """
                    ctx._source.whois = params.whois;
                """,
                "params": {"whois": whois},
            },
        )


class Command(BaseCommand):
    help = "Annotate events in Elasticsearch"

    source_choices = [
        "whois",
    ]

    def add_arguments(self, parser):
        parser.add_argument(
            "--source",
            type=str,
            choices=self.source_choices,
            required=True,
            help="Source(s) of events to annotate",
        )
        parser.add_argument(
            "--limit",
            type=int,
            default=1000,
            help="Maximum number of unique IPs to annotate (default: 1000)",
        )

    def handle(self, *args, **options):  # NOQA: C901

        source = options["source"]
        limit = options["limit"]

        whois = CachedWhois()
        es = EsService()

        cnt = 0
        cnt_total = 0

        for r in es.iter_top_ips(size=limit):
            ip = r[0]
            count = r[1]
            print(f"Annotating IP {ip} - {count}")

            info = whois(ip)



            cnt += 1
            cnt_total += count

            if not info:
                print(f"Failed to get whois info for IP {ip}")
                continue

            es.update_ip(ip, info)

        self.stdout.write(f"annotated: {source} - {cnt} unique IPs - {cnt_total} total events")