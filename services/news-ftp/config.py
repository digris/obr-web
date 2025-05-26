import pathlib
import logging.config

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class FTPUser(BaseModel):
    login: str
    password: str
    homedir: pathlib.Path
    perm: str = "elradfmwT"


class Settings(BaseSettings):

    """
    FTP_USERS format:
    login:password:/relative/path/to/homedir,login2:password2:/another/relative/path,...
    """

    debug: bool = False
    ftp_base_dir: pathlib.Path = "/data/news-ftp"
    ftp_host: str = "0.0.0.0"
    ftp_port: int = 21
    ftp_passive_ports: tuple[int, int] | None = (60000, 65535)
    ftp_masquerade_address: str | None = None
    ftp_users: str = ""  # RAW value, see below for parsing
    api_token: str = "---CHANGE-ME---"
    model_config = SettingsConfigDict(env_file=".env")

    @property
    def ftp_user_list(self) -> list[FTPUser]:
        users = []

        if not self.ftp_users:
            raise ValueError("FTP_USERS is required and cannot be empty.")

        for entry in self.ftp_users.split(","):
            try:
                login, password, rel_dir = entry.strip().split(":")

                raw_homedir = self.ftp_base_dir / rel_dir.lstrip("/")
                homedir = raw_homedir.resolve(strict=False)

                # validate chroot: must be inside ftp_base_dir
                if not homedir.is_relative_to(self.ftp_base_dir.resolve()):
                    raise ValueError(f"homedir {homedir} is outside ftp_base_dir")

                users.append(
                    FTPUser(
                        login=login,
                        password=password,
                        homedir=homedir,
                    )
                )

            except ValueError:
                raise ValueError(f"Invalid FTP_USERS entry: {entry}")

        return users


settings = Settings()

print(settings.ftp_user_list)


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {"format": "%(levelname)-8s%(name)s:%(funcName)s: %(message)s"},
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
    },
    "root": {
        "level": "WARNING",
        "handlers": ["console"],
    },
    "loggers": {
        "aioftp": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
        "ftp_server": {
            "level": "DEBUG",
            "handlers": ["console"],
            "propagate": False,
        },
    },
}

logging.config.dictConfig(LOGGING_CONFIG)
