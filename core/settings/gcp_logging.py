import google.cloud.logging

client = google.cloud.logging.Client()
client.setup_logging()


LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "propagate": False,
    "root": {
        "level": "WARNING",
        "handlers": [
            "gcp",
        ],
    },
    "handlers": {
        "gcp": {
            "level": "DEBUG",
            "class": "google.cloud.logging.handlers.CloudLoggingHandler",
            "client": client,
        },
    },
    "loggers": {
        "django.db.backends": {
            "level": "WARNING",
            "handlers": [
                "gcp",
            ],
            "propagate": False,
        },
        "django.request": {
            "level": "DEBUG",
            "handlers": [
                "gcp",
            ],
            "propagate": False,
        },
        "user_identity": {
            "level": "DEBUG",
            "handlers": [
                "gcp",
            ],
            "propagate": False,
        },
        "account": {
            "level": "DEBUG",
            "handlers": [
                "gcp",
            ],
            "propagate": False,
        },
        "geoip": {
            "level": "DEBUG",
            "handlers": [
                "gcp",
            ],
            "propagate": False,
        },
        "catalog": {
            "level": "DEBUG",
            "handlers": [
                "gcp",
            ],
            "propagate": False,
        },
        "stats": {
            "level": "DEBUG",
            "handlers": [
                "gcp",
            ],
            "propagate": False,
        },
        "sync": {
            "level": "DEBUG",
            "handlers": [
                "gcp",
            ],
            "propagate": False,
        },
        "broadcast": {
            "level": "DEBUG",
            "handlers": [
                "gcp",
            ],
            "propagate": False,
        },
        "spa": {
            "level": "DEBUG",
            "handlers": [
                "gcp",
            ],
            "propagate": False,
        },
    },
}
