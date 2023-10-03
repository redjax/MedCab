from __future__ import annotations

import socket

import attrs
from attrs import define, field

from dynaconf import settings

from flask import Flask
from flask.logging import default_handler

from medcab_backend.constants import (
    APP_DEBUG,
    APP_HOST,
    APP_PORT,
    CONTAINER_ENV,
    ENV,
    owm_conf,
)
from medcab_backend.main import app

# from medcab_backend.utils.flask_utils import setup_flask_logger
from loguru import logger as log
from red_utils.ext.loguru_utils import init_logger, sinks

port_ban_list: list[int] = [1, 22, 80, 443, 21]


def get_free_port() -> int:
    """Use sockets to get a random, free tcp port.

    If that port is in a pre-set list of "banned" ports (i.e. 22, which is for SSH),
    get a new port.
    """
    sock = socket.socket()
    sock.bind(("", 0))
    port = sock.getsockname()[1]

    if port not in port_ban_list:
        log.debug(f"Port [{port}] is free and not in list of banned ports")
        return port
    else:
        log.debug(f"Port :{port} is taken or reserved. Getting new port.")
        get_free_port()


@define
class FlaskServer:
    flask_app: Flask = field(default=app)
    flask_debug: bool = field(default=APP_DEBUG)
    flask_host: str = field(default=APP_HOST)
    flask_port: int = field(default=APP_PORT)

    def run_server(self):
        try:
            self.flask_app.run(
                debug=self.flask_debug, host=self.flask_host, port=self.flask_port
            )
        except Exception as exc:
            raise Exception(
                f"Unhandled exception starting Flask server. Details: {exc}"
            )


if __name__ == "__main__":
    ## Override Flask app's default logger with Loguru
    # setup_flask_logger(app=app)
    init_logger(sinks=[sinks.default_stdout_color_sink])

    log.info(f"[{ENV}] Starting app")
    log.info(f"[{ENV}] Settings: {settings.as_dict()}")

    server = FlaskServer()

    try:
        server.run_server()
    except Exception as exc:
        log.error(Exception(f"Unhandled exception starting app. Details: {exc}"))

        port = get_free_port()
        server.flask_port = port
        log.debug(f"Retrying on port :{server.flask_port}")

        server.run_server()
