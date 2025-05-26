#!/usr/bin/env python3
import pathlib
import logging
import pyftpdlib.authorizers
import pyftpdlib.handlers
import pyftpdlib.servers

from config import settings

LOGGER = logging.getLogger("ftp_server")


class ServerHandler(
    pyftpdlib.handlers.FTPHandler,
):

    def on_file_received(self, file_path):

        path = pathlib.Path(file_path)

        print("file_path", path, type(path))

        LOGGER.info(f"upload complete: {str(path)}")


def start_ftp_server(
    host: str = "127.0.0.1",
    port: int = 21,
    passive_ports: tuple[int, int] | None = None,
    masquerade_address: str | None = None,
):

    authorizer = pyftpdlib.authorizers.DummyAuthorizer()

    for user in settings.ftp_user_list:
        authorizer.add_user(
            user.login,
            user.password,
            homedir=user.homedir,
            perm=user.perm,
        )

    handler = ServerHandler
    handler.authorizer = authorizer

    handler.banner = "OBR - News FTP Server"

    if passive_ports and len(passive_ports) == 2:
        handler.passive_ports = range(*passive_ports)

    if masquerade_address:
        handler.masquerade_address = masquerade_address

    server = pyftpdlib.servers.FTPServer(
        (host, port),
        handler,
    )

    server.max_cons = 300
    server.max_cons_per_ip = 10

    LOGGER.info(f"starting FTP server on: {host}:{port} - passive ports: {passive_ports}")

    server.serve_forever()


if __name__ == "__main__":
    start_ftp_server(
        host=settings.ftp_host,
        port=settings.ftp_port,
        passive_ports=settings.ftp_passive_ports,
        masquerade_address=settings.ftp_masquerade_address,
    )
