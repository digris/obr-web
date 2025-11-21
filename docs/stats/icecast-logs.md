# Icecast2 Compatible Log Exporter

For listener statistics [radio-data.ch](https://radio-data.ch/) we have to provide logs in a format
compatible with Icecast2 log files.

```shell
./obr-cli stats_export_icecast_logs --help
```

```shell
./obr-cli stats_export_icecast_logs \
  --date-from 2023-01-01 \
  --date-until 2025-12-31 \
  --dst-dir data/logs/ \
  --database sync \
  --origin hls icecast \
  --filename-prefix obr
```

## Quick Plausibility Check

```shell
goaccess data/logs/* \                                                                                                                                                                                                                                                                                      main ✭ ✚ ✖ ✱
  --log-format='%h - %^[%d:%t %^] "%r" %s %b "%R" "%u" %T' \
  --date-format='%d/%b/%Y' \
  --time-format='%T' \
  -o data/logs/report.html
```
