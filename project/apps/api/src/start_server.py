from __future__ import annotations

import sys

import stackprinter

stackprinter.set_excepthook(style="darkbg2")

from pathlib import Path

from core.config import api_settings, app_settings
from loguru import logger as log
from pydantic import BaseModel
from red_utils.ext.fastapi_utils import setup_uvicorn_logging
from red_utils.ext.loguru_utils import init_logger
import uvicorn

ENV: str = app_settings.env
CONTAINER_ENV: bool = app_settings.container_env
env_string: str = f"[env:{ENV.upper()}|container:{CONTAINER_ENV}]"

if __name__ == "__main__":
    ## If this file was run directly, initialize logger.
    init_logger()
    ## Configure Uvicorn logging
    setup_uvicorn_logging(level=app_settings.log_level)


class UvicornCustomServer(BaseModel):
    """Customize a Uvicorn server by passing a dict
    to UvicornCustomServer.parse_obj(dict).

    Run server with instance's .run_server(). This function
    builds a Uvicorn server with the config on the instance,
    then runs it.
    """

    app: str = "main:app"
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = False
    root_path: str = "/"

    def run_server(self) -> None:
        uvicorn.run(
            app=self.app,
            host=self.host,
            port=self.port,
            reload=self.reload,
            root_path=self.root_path,
        )


_uvi_dev_conf = {
    "app": "api.main:app",
    "host": "0.0.0.0",
    "port": 8000,
    "reload": True,
    "root_path": "/api/v1",
    "debug": True,
}

# dev_server = UvicornCustomServer.parse_obj(_uvi_dev_conf)
dev_server = UvicornCustomServer.model_validate(_uvi_dev_conf)
prod_server = UvicornCustomServer()


if __name__ == "__main__":
    match ENV:
        case "dev":
            server = dev_server
        case "prod":
            server = prod_server
        case _:
            server = prod_server

    log.info(f"Starting Uvicorn server | {env_string}")
    log.debug(f"Uvicorn config: {server}")

    log.debug(f"Serving app {server.app} on port {server.port}")
    server.run_server()
