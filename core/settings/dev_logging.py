LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "root": {
        "level": "WARNING",
        "handlers": ["console"],
    },
    "formatters": {
        "default": {
            "format": "%(levelname)-8s %(name)s %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
    },
    "loggers": {
        "django.db.backends": {
            "level": "WARNING",
            "handlers": [
                "console",
            ],
            "propagate": False,
        },
        "django.request": {
            "level": "DEBUG",
            "handlers": [
                "console",
            ],
            "propagate": False,
        },
        "user_identity": {
            "level": "DEBUG",
            "handlers": [
                "console",
            ],
            "propagate": False,
        },
        "account": {
            "level": "DEBUG",
            "handlers": [
                "console",
            ],
            "propagate": False,
        },
        "geoip": {
            "level": "DEBUG",
            "handlers": [
                "console",
            ],
            "propagate": False,
        },
        "catalog": {
            "level": "DEBUG",
            "handlers": [
                "console",
            ],
            "propagate": False,
        },
        "tagging": {
            "level": "INFO",
            "handlers": [
                "console",
            ],
            "propagate": False,
        },
        "stats": {
            "level": "DEBUG",
            "handlers": [
                "console",
            ],
            "propagate": False,
        },
        "sync": {
            "level": "INFO",
            "handlers": [
                "console",
            ],
            "propagate": False,
        },
        "broadcast": {
            "level": "DEBUG",
            "handlers": [
                "console",
            ],
            "propagate": False,
        },
        "spa": {
            "level": "DEBUG",
            "handlers": [
                "console",
            ],
            "propagate": False,
        },
    },
}
