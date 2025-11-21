import datetime
import hashlib
import ipaddress
import logging
import pathlib

from stats.models import StreamEvent

logger = logging.getLogger(__name__)


class ExporterError(Exception):
    pass


class DailyFileWriter:

    dst_dir: pathlib.Path
    filename_tpl: str
    current_date: datetime.date | None
    fp: pathlib.Path | None
    files_written: list[pathlib.Path]

    def __init__(self, dst_dir: pathlib.Path, filename_tpl: str):
        self.dst_dir = dst_dir
        self.filename_tpl = filename_tpl
        self.current_date = None
        self.fp = None
        self.files_written = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        if self.fp:
            self.fp.close()
            self.fp = None
        return False

    def rotate(self, day) -> None:
        if self.fp:
            self.fp.close()

        filename = self.filename_tpl.format(date=day.strftime("%Y-%m-%d"))
        path = self.dst_dir / filename
        self.fp = open(  # NOQA SIM115 - here we need this pattern
            path,
            "w",
            encoding="utf-8",
        )
        self.current_date = day

        logger.debug(f"opened log file: {path}")

        self.files_written.append(path)

    def write_for_date(self, day: datetime.date, line: str):
        if self.current_date != day:
            self.rotate(day)
        self.fp.write(line + "\n")


class LogExporter:

    dst: pathlib.Path
    filename_prefix: str | None
    anonymize_ip: bool
    include_user: bool
    database: str

    log_line_tpl: str = (
        '{ip} - {user}- [{time}] "{method} {path} {protocol}" {status} {bytes_sent} "{referrer}" "{user_agent}" {seconds_connected}'
    )

    log_filename_tpl: str = "{date}-icecast2-compatible.log"

    def __init__(
        self,
        *,
        dst_dir: pathlib.Path,
        filename_prefix: str | None = None,
        anonymize_ip: bool = False,
        include_user: bool = False,
        database: str = "default",
    ) -> None:

        if not dst_dir.is_dir():
            raise ExporterError(f"not a directory: {dst_dir}")

        self.dst = dst_dir
        self.anonymize_ip = anonymize_ip
        self.include_user = include_user
        self.database = database

        if filename_prefix:
            self.log_filename_tpl = filename_prefix + "-" + self.log_filename_tpl

        logger.debug(
            f"LogExporter initialized with dst_dir={dst_dir}, tpl={self.log_filename_tpl}, database={database}",
        )

    @staticmethod
    def date_to_utc_day(date: datetime.date) -> datetime.datetime:

        if not isinstance(date, datetime.date):
            raise ValueError("expected date")

        return datetime.datetime.combine(date, datetime.time.min, tzinfo=datetime.UTC)

    @staticmethod
    def mask_ip(ip_str: str) -> str:
        try:
            addr = ipaddress.ip_address(ip_str)
        except ValueError:
            return "0.0.0.0"  # NOQA S104

        if isinstance(addr, ipaddress.IPv4Address):
            masked = int(addr) & 0xFFFFFF00
            return str(ipaddress.IPv4Address(masked))

        if isinstance(addr, ipaddress.IPv6Address):
            masked = int(addr) & ((1 << 128) - (1 << 80))
            return str(ipaddress.IPv6Address(masked))

        return "0.0.0.0"  # NOQA S104

    def event_to_log_line(self, event: StreamEvent) -> str:
        """
        example lines:
        127.0.0.11 - - [09/May/2025:23:58:17 +0000] "GET /320.mp3 HTTP/1.1" 200 73227 "-" "Go-http-client/1.1" 1
        34.14.14.3 - - [21/Nov/2025:12:25:01 +0000] "GET /320.mp3 HTTP/1.1" 200 66003 "-" "Go-http-client/1.1" 0
        80.99.131.227 - - [21/Nov/2025:12:29:08 +0000] "GET /16bit.flac HTTP/1.1" 200 354216 "-" "ExoPlayer/2.19.1 (Linux;Android 15) ExoPlayerLib/2.19.1" 7
        """

        if self.anonymize_ip:
            ip = self.mask_ip(event.ip) if event.ip else "0.0.0.0"  # NOQA S104
        else:
            ip = event.ip or "0.0.0.0"  # NOQA S104
        if self.include_user:
            user = (
                hashlib.sha256(event.device_key.encode("utf-8")).hexdigest() + " "
                if event.device_key
                else ""
            )
        else:
            user = ""
        time = event.time_end.strftime("%d/%b/%Y:%H:%M:%S %z")
        method = event.method or "-"
        path = event.path or "GET"
        protocol = "HTTP/1.1"
        status = event.status or 200
        bytes_sent = event.bytes_sent or 0
        referrer = event.referer or "-"
        user_agent = event.user_agent or "-"
        seconds_connected = (
            int(event.seconds_connected) if event.seconds_connected else 0
        )

        return self.log_line_tpl.format(
            ip=ip,
            user=user,
            time=time,
            method=method,
            path=path,
            protocol=protocol,
            status=status,
            bytes_sent=bytes_sent,
            referrer=referrer,
            user_agent=user_agent,
            seconds_connected=seconds_connected,
        )

    def export(
        self,
        *,
        date_from: datetime.date,
        date_until: datetime.date,
        filter_origin: list[str] = None,
    ) -> list[pathlib.Path]:

        utc_time_from = self.date_to_utc_day(date_from)
        utc_time_until = (
            self.date_to_utc_day(date_until)
            + datetime.timedelta(days=1)
            - datetime.timedelta(microseconds=1)
        )

        filter_origin = filter_origin if filter_origin is not None else []

        qs = StreamEvent.objects.filter(
            time_start__gte=utc_time_from,
            time_end__lte=utc_time_until,
        ).order_by("time_end")

        if filter_origin:
            qs = qs.filter(origin__in=filter_origin)

        files_written = []

        with DailyFileWriter(self.dst, self.log_filename_tpl) as writer:

            for event in qs.using(self.database).iterator():
                day = event.time_end.date()
                line = self.event_to_log_line(event)
                writer.write_for_date(day, line)

            files_written = writer.files_written

        return files_written


def icecast_log_export(
    *,
    date_from: datetime.datetime,
    date_until: datetime.datetime,
    dst_dir: pathlib.Path,
    filename_prefix: str | None = None,
    anonymize_ip: bool = False,
    include_user: bool = False,
    origin: list[str] = None,
    database: str = "default",
) -> list[pathlib.Path]:

    exporter = LogExporter(
        dst_dir=dst_dir,
        filename_prefix=filename_prefix,
        anonymize_ip=anonymize_ip,
        include_user=include_user,
        database=database,
    )

    return exporter.export(
        date_from=date_from,
        date_until=date_until,
        filter_origin=origin or [],
    )
