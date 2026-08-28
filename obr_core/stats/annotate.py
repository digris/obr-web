import json
import logging
import pathlib
import sqlite3
from ipaddress import ip_address, ip_network

from django.conf import settings

import elasticsearch
from ipregistry import IpregistryClient, IpregistryConfig
from ipregistry.model import ApiError as IpregistryApiError
from ipwhois import IPWhois

ES_API_URL = settings.STATS_ES_API_URL
ES_API_KEY = settings.STATS_ES_API_KEY

ES_INDEX = "listener-sessions"

IPREGISTRY_API_KEY = settings.IPREGISTRY_API_KEY

SQLITE_CACHE = settings.PROJECT_ROOT / "data" / "stats" / "annotate-cache.sqlite3"


LOGGER = logging.getLogger(__name__)


class CachedWhois:

    db_table = "whois_cache"

    LOGGER = logging.getLogger(f"{__name__}.CachedWhois")

    def __init__(self, db_path: pathlib.Path):
        self.cache: dict[str, dict] = {}

        self.db = sqlite3.connect(db_path)
        self.db.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {self.db_table} (
                cidr TEXT PRIMARY KEY,
                data TEXT NOT NULL
            )
        """,
        )
        self.db.commit()

        self.cache_load()

    ###################################################################
    # cache
    ###################################################################
    def cache_load(self):
        self.cache = {}

        for cidr, data in self.db.execute(f"SELECT cidr, data FROM {self.db_table}"):
            self.cache[cidr] = json.loads(data)
        self.LOGGER.debug("Loaded %s WHOIS cache entries", len(self.cache))

    def cache_reset(self):
        self.cache = {}
        self.db.execute(f"DELETE FROM {self.db_table}")
        self.db.commit()
        self.LOGGER.info("Reset WHOIS cache")

    def cache_get(self, ip: str):
        addr = ip_address(ip)

        for cidr, data in self.cache.items():
            if addr in ip_network(cidr, strict=False):
                self.LOGGER.debug("WHOIS cache hit for %s in %s", ip, cidr)
                return data

        return None

    def cache_set(self, cidr: str | None, data: dict | None):
        if not cidr or not data:
            return

        self.cache[cidr] = data

        self.db.execute(
            f"INSERT OR REPLACE INTO {self.db_table} (cidr, data) VALUES (?, ?)",
            (cidr, json.dumps(data)),
        )
        self.db.commit()
        self.LOGGER.debug("Stored WHOIS cache entry for %s", cidr)

    ###################################################################
    # mapping / parsing
    ###################################################################
    @staticmethod
    def cidr_candidates(value: str | None):
        if not value or value == "NA":
            return []

        candidates = []
        for cidr in value.split(","):
            cidr = cidr.strip()
            if not cidr:
                continue
            try:
                candidates.append(ip_network(cidr, strict=False))
            except ValueError:
                continue

        return candidates

    @classmethod
    def best_cidr(cls, ip: str | None, *values: str | None):
        networks = []

        for value in values:
            networks.extend(cls.cidr_candidates(value))

        if ip:
            addr = ip_address(ip)
            networks = [network for network in networks if addr in network]

        if not networks:
            return None

        return str(max(networks, key=lambda network: network.prefixlen))

    @staticmethod
    def registrant_name(objects):
        for obj in (objects or {}).values():
            if "registrant" not in (obj.get("roles") or []):
                continue

            contact = obj.get("contact") or {}
            if name := contact.get("name"):
                return name

        return None

    def parse_whois_result(self, res):
        network = res.get("network") or {}
        query_ip = res.get("query")
        asn_cidr = self.best_cidr(query_ip, res.get("asn_cidr"))
        net_cidr = self.best_cidr(query_ip, network.get("cidr"))
        cidr = net_cidr or asn_cidr

        if not cidr:
            self.LOGGER.warning("RDAP lookup returned no usable CIDR: %s", res)
            return None, None

        return cidr, {
            "source": "ipwhois_rdap",
            "rir": res.get("asn_registry"),
            "cidr": cidr,
            "asn_cidr": asn_cidr,
            "net_cidr": net_cidr,
            "asn": int(res["asn"]) if str(res.get("asn", "")).isdigit() else None,
            "asn_description": res.get("asn_description"),
            "asn_country_code": res.get("asn_country_code"),
            "net_name": network.get("name"),
            "net_type": network.get("type"),
            "net_country": network.get("country"),
            "net_parent": network.get("parent_handle"),
            "registrant": self.registrant_name(res.get("objects")),
        }

    ###################################################################
    # entry point
    ###################################################################
    @staticmethod
    def is_public_ip(ip):
        return not (
            ip.is_private
            or ip.is_loopback
            or ip.is_link_local
            or ip.is_multicast
            or ip.is_reserved
            or ip.is_unspecified
        )

    def __call__(self, ip: str):
        try:
            addr = ip_address(ip)
        except ValueError:
            self.LOGGER.warning("Invalid IP address: %s", ip)
            return None

        if not self.is_public_ip(addr):
            self.LOGGER.info("Skipping non-public IP address: %s", addr)
            return None

        ip = str(addr)

        # 1) cache hit by containing CIDR
        if res := self.cache_get(ip):
            return res

        # 2) RDAP lookup
        try:
            self.LOGGER.debug("Running WHOIS RDAP lookup for %s", ip)
            whois_res = IPWhois(ip, timeout=2).lookup_rdap(depth=1, inc_nir=False)
        except Exception as e:  # noqa: BLE001
            self.LOGGER.exception("WHOIS RDAP lookup failed for %s: %s", ip, e)
            return None

        self.LOGGER.debug(
            "WHOIS RDAP lookup result for %s: ASN %s, ASN CIDR %s",
            ip,
            whois_res.get("asn"),
            whois_res.get("asn_cidr"),
        )

        # 3) parse / map
        cidr, res = self.parse_whois_result(whois_res)

        # 4) update cache
        self.cache_set(cidr, res)

        return res


class CachedIPIntel:

    db_table = "ipintel_cache"

    LOGGER = logging.getLogger(f"{__name__}.CachedIPIntel")

    def __init__(self, api_key: str, db_path: pathlib.Path):

        self.cache: dict[str, dict] = {}

        self.ipreg_client = IpregistryClient(
            IpregistryConfig(
                api_key,
                timeout=5,
            ).with_eu_base_url(),
        )

        self.db = sqlite3.connect(db_path)
        self.db.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {self.db_table} (
                ip TEXT PRIMARY KEY,
                data TEXT NOT NULL
            )
        """,
        )
        self.db.commit()

        self.cache_load()

    ###################################################################
    # cache
    ###################################################################
    def cache_load(self):
        for ip, data in self.db.execute(f"SELECT ip, data FROM {self.db_table}"):
            self.cache[ip] = json.loads(data)
        self.LOGGER.debug("Loaded %s IPIntel cache entries", len(self.cache))

    def cache_reset(self):
        self.cache = {}
        self.db.execute(f"DELETE FROM {self.db_table}")
        self.db.commit()
        self.LOGGER.info("Reset IPIntel cache")

    def cache_get(self, ip: str):
        if ip in self.cache:
            self.LOGGER.debug("IPIntel cache hit for %s", ip)
            return self.cache[ip]
        row = self.db.execute(
            f"SELECT data FROM {self.db_table} WHERE ip = ?",
            (ip,),
        ).fetchone()
        if not row:
            return None

        data = json.loads(row[0])
        self.cache[ip] = data
        return data

    def cache_set(self, ip: str, data: dict):
        self.cache[ip] = data
        self.db.execute(
            f"INSERT OR REPLACE INTO {self.db_table} (ip, data) VALUES (?, ?)",
            (str(ip), json.dumps(data)),
        )
        self.db.commit()
        self.LOGGER.debug("Stored IPIntel cache entry for %s", ip)

    @staticmethod
    def parse_tags(sec):  # noqa: C901
        tags = []
        if sec.is_anonymous:
            tags.append("anonymous")
        if sec.is_proxy:
            tags.append("proxy")
        if sec.is_relay:
            tags.append("relay")
        if sec.is_vpn:
            tags.append("vpn")
        if sec.is_tor or sec.is_tor_exit:
            tags.append("tor")
        if sec.is_cloud_provider:
            tags.append("cloud-provider")
        if sec.is_abuser:
            tags.append("abuse")
        if sec.is_attacker:
            tags.append("attacker")
        if sec.is_threat:
            tags.append("threat")
        if sec.is_bogon:
            tags.append("bogon")
        return tags

    @staticmethod
    def parse_access(carrier, conn, sec):
        if sec.is_bogon:
            return "bogon"
        if sec.is_tor or sec.is_tor_exit:
            return "tor"
        if sec.is_vpn:
            return "vpn"
        if sec.is_proxy or sec.is_relay or sec.is_anonymous:
            return "proxy"
        if sec.is_cloud_provider:
            return "cloud-provider"
        if carrier.name or carrier.mcc or carrier.mnc:
            return "mobile"
        if conn.type == "isp":
            return "fixed"
        return conn.type or "unknown"

    def parse_ipreg_result(self, res):
        api_credits = res.credits
        data = res.data

        """
        data shape
        stuff we don't care already removed from example response

        {'carrier': {'mcc': None, 'mnc': None, 'name': None},
        'company': {'domain': 'netutils.io',
                    'name': 'Internet Utilities Na LLC',
                    'type': 'business'},
        'connection': {'asn': 834,
                        'domain': 'ipxo.com',
                        'organization': 'IPXO LLC',
                        'route': '40.183.112.0/20',
                        'type': 'hosting'},
        'hostname': None,
        'ip': '40.183.117.224',
        'location': {'city': 'Washington',
                    'continent': {'code': 'NA', 'name': 'North America'},
                    'country': {'code': 'US',
                                'name': 'United States',
                    'in_eu': False,
                    'language': {'code': 'en',
                                'name': 'English',
                                'native': 'English'},
                    'latitude': 33.73684,
                    'longitude': -82.73938,
                    'postal': '30673',
                    'region': {'code': 'US-GA', 'name': 'Georgia'}},
        'security': {'is_abuser': False,
                    'is_anonymous': True,
                    'is_attacker': False,
                    'is_bogon': False,
                    'is_cloud_provider': True,
                    'is_proxy': True,
                    'is_relay': False,
                    'is_threat': False,
                    'is_tor': False,
                    'is_tor_exit': False,
                    'is_vpn': False},
        'time_zone': {'abbreviation': 'EST',
                    'current_time': '2026-06-19T08:57:34-04:00',
                    'id': 'America/New_York',
                    'in_daylight_saving': True,
                    'name': 'Eastern Standard Time',
                    'offset': -14400},
        'type': 'IPv4'}

        """

        if api_credits.remaining % 100 == 0:
            self.LOGGER.info(
                "IPIntel lookup credits: %s remaining",
                api_credits.remaining,
            )

        carrier = data.carrier
        company = data.company
        conn = data.connection
        loc = data.location
        sec = data.security
        time_zone = data.time_zone

        parsed = {
            "source": "ipregistry",
            "provider": conn.organization,  # Swisscom (schweiz) AG
            "net_asn": conn.asn,
            "net_type": conn.type,
            "net_domain": conn.domain,
            "org_name": company.name,  # Bluewin Is An Lir And ISP in Switzerland.
            "org_type": company.type,
            "org_domain": company.domain,
            "loc_country": loc.country.code,
            "loc_region": loc.region.code,
            "loc_city": loc.city,
            "loc_zip_code": loc.postal,
            "loc_coordinates": (
                {"lat": loc.latitude, "lon": loc.longitude}
                if loc.latitude is not None and loc.longitude is not None
                else None
            ),
            "tz_code": time_zone.abbreviation,
            "access": self.parse_access(carrier, conn, sec),
            "tags": self.parse_tags(sec),
            "mobile": (
                {
                    "operator": carrier.name,
                    "mcc": carrier.mcc,
                    "mnc": carrier.mnc,
                }
                if carrier.name
                else None
            ),
        }

        return parsed

    ###################################################################
    # entry point
    ###################################################################
    def __call__(self, ip: str):
        try:
            ip = str(ip_address(ip))
        except ValueError:
            self.LOGGER.warning("Invalid IP address: %s", ip)
            return None

        # 1) cache hit
        if res := self.cache_get(ip):
            return res

        # 2) IPIntel lookup
        try:
            ipreg_res = self.ipreg_client.lookup_ip(ip)
        except IpregistryApiError as e:
            if e.code == "RESERVED_IP_ADDRESS":
                self.LOGGER.info("Skipping reserved IP address: %s", ip)
                ipreg_res = None
            else:
                raise e

        # 3) parse / map
        res = self.parse_ipreg_result(ipreg_res) if ipreg_res else None

        # 4) update cache
        self.cache_set(ip, res)
        return res


class EsService:
    client: elasticsearch.Elasticsearch

    def __init__(self, index: str, api_url: str, api_key: str):

        self.index = index

        self.client = elasticsearch.Elasticsearch(
            api_url,
            api_key=api_key,
            verify_certs=False,
            ssl_show_warn=False,
            request_timeout=10,
        )

    def iter_top_ips(self, must_not_exists: str, size=10):

        if must_not_exists not in ["whois.rir", "ipintel.source"]:
            raise ValueError(f"Invalid must_not_exists field: {must_not_exists}")

        resp = self.client.search(
            index=self.index,
            size=0,
            aggs={
                "top_ips": {
                    "terms": {
                        "field": "remote_addr",
                        "size": size,
                        "order": {"_count": "desc"},
                    },
                },
            },
            query={
                "bool": {
                    "must": [
                        {"range": {"duration_s": {"gte": 10}}},
                        {"range": {"time_start": {"gte": "2025-01-01T00:00:00"}}},
                    ],
                    "must_not": [{"exists": {"field": must_not_exists}}],
                },
            },
        )

        for b in resp["aggregations"]["top_ips"]["buckets"]:
            yield b["key"], b["doc_count"]

    def update_whois(self, ip, whois: dict):
        self.client.update_by_query(
            index=self.index,
            conflicts="proceed",
            refresh=False,
            wait_for_completion=False,
            requests_per_second=50,
            query={
                "bool": {
                    "must": [
                        {"term": {"remote_addr": ip}},
                    ],
                    "must_not": [{"exists": {"field": "whois.rir"}}],
                },
            },
            script={
                "source": """
                    ctx._source.whois = params.whois;
                """,
                "params": {"whois": whois},
            },
        )

    def update_ipintel(self, ip, ipintel: dict):
        self.client.update_by_query(
            index=self.index,
            conflicts="proceed",
            refresh=False,
            wait_for_completion=False,
            requests_per_second=50,
            query={
                "bool": {
                    "must": [
                        {"term": {"remote_addr": ip}},
                    ],
                    "must_not": [{"exists": {"field": "ipintel.source"}}],
                },
            },
            script={
                "source": """
                    ctx._source.ipintel = params.ipintel;
                """,
                "params": {"ipintel": ipintel},
            },
        )


def annotate_whois(*, limit=10, reset_cache=False):

    es = EsService(
        index=ES_INDEX,
        api_url=ES_API_URL,
        api_key=ES_API_KEY,
    )
    whois = CachedWhois(
        db_path=SQLITE_CACHE,
    )

    if reset_cache:
        whois.cache_reset()

    cnt = 0
    cnt_toal = 0

    for r in es.iter_top_ips(must_not_exists="whois.rir", size=limit):
        ip = r[0]
        count = r[1]

        LOGGER.info("Running WHOIS lookup for %s (%s sessions)", ip, count)

        whois_res = whois(ip)

        cnt += 1
        cnt_toal += count

        if not whois_res:
            LOGGER.warning("Failed to get WHOIS info for %s", ip)
            continue

        es.update_whois(ip, whois_res)

    return cnt, cnt_toal


def annotate_ipintel(*, limit=10, reset_cache=False):

    es = EsService(
        index=ES_INDEX,
        api_url=ES_API_URL,
        api_key=ES_API_KEY,
    )
    ipintel = CachedIPIntel(
        api_key=IPREGISTRY_API_KEY,
        db_path=SQLITE_CACHE,
    )

    if reset_cache:
        ipintel.cache_reset()

    cnt = 0
    cnt_toal = 0

    for r in es.iter_top_ips(must_not_exists="ipintel.source", size=limit):
        ip = r[0]
        count = r[1]

        LOGGER.info("Running IPIntel lookup for %s (%s sessions)", ip, count)

        ipintel_res = ipintel(ip)

        cnt += 1
        cnt_toal += count

        if not ipintel_res:
            LOGGER.warning("Failed to get IPIntel info for %s", ip)
            continue

        es.update_ipintel(ip, ipintel_res)

    return cnt, cnt_toal
