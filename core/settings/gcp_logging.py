import logging

from google.cloud import logging as google_cloud_logging

gcp_log_client = google_cloud_logging.Client()
gcp_log_client.setup_logging()


class StructuredFormatter(logging.Formatter):
    def format(self, record):
        message = super().format(record)
        meta = {
            "module": record.module,
            "funcName": record.funcName,
            "filename": record.filename,
            "lineno": record.lineno,
        }
        if record.args:
            try:
                return dict({"text": message, "meta": meta, **record.args})
            except TypeError:
                return dict({"text": message, "meta": meta, "args": record.args})
        return {"text": message, "meta": meta}


LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "propagate": False,
    "root": {
        "level": "WARNING",
        "handlers": [
            "console",
            "gcp",
        ],
    },
    "formatters": {
        "verbose": {
            "format": "%(asctime)s %(levelname)s\t%(name)s\t%(funcName)s:%(lineno)s - %(message)s",
        },
        "gcp": {
            "class": "settings.gcp_logging.StructuredFormatter",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "gcp": {
            "level": "DEBUG",
            "class": "google.cloud.logging.handlers.CloudLoggingHandler",
            "client": gcp_log_client,
            "formatter": "gcp",
        },
    },
    "loggers": {
        "django.db.backends": {
            "level": "WARNING",
            "handlers": [
                "console",
                "gcp",
            ],
            "propagate": False,
        },
        "django.request": {
            "level": "DEBUG",
            "handlers": [
                "console",
                "gcp",
            ],
            "propagate": False,
        },
        "user_identity": {
            "level": "DEBUG",
            "handlers": [
                "console",
                "gcp",
            ],
            "propagate": False,
        },
        "account": {
            "level": "DEBUG",
            "handlers": [
                "console",
                "gcp",
            ],
            "propagate": False,
        },
        "geoip": {
            "level": "DEBUG",
            "handlers": [
                "console",
                "gcp",
            ],
            "propagate": False,
        },
        "catalog": {
            "level": "DEBUG",
            "handlers": [
                "console",
                "gcp",
            ],
            "propagate": False,
        },
        "stats": {
            "level": "DEBUG",
            "handlers": [
                "console",
                "gcp",
            ],
            "propagate": False,
        },
        "sync": {
            "level": "DEBUG",
            "handlers": [
                "console",
                "gcp",
            ],
            "propagate": False,
        },
        "broadcast": {
            "level": "DEBUG",
            "handlers": [
                "console",
                "gcp",
            ],
            "propagate": False,
        },
        "spa": {
            "level": "DEBUG",
            "handlers": [
                "console",
                "gcp",
            ],
            "propagate": False,
        },
    },
}
