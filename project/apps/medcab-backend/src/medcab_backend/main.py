from dynaconf import settings

from loguru import logger as log
from red_utils.ext.loguru_utils import init_logger, sinks

from flask import Flask

from medcab_backend.constants import (
    ENV,
    CONTAINER_ENV,
    APP_NAME,
    APP_VERSION,
    APP_DESCRIPTION,
)

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index() -> dict[str, str]:
    log.debug(f"MedCab Backend root page reached")
    return {"msg": f"{APP_NAME} v{APP_VERSION} reached"}


if __name__ == "__main__":
    log.debug(f"Settings: {settings.as_dict()}")
