import sys

sys.path.append(".")

from pathlib import Path

from core import app_settings, api_settings

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from red_utils.ext.loguru_utils import (
    init_logger,
    LoguruSinkStdOut,
    LoguruSinkAppFile,
    LoguruSinkErrFile,
)
from red_utils.ext.fastapi_utils import (
    default_api_str,
    default_openapi_url,
    get_app,
    healthcheck,
    logging_dependency,
    tags_metadata,
    update_tags_metadata,
    fix_api_docs,
    setup_uvicorn_logging,
)
from red_utils.ext.fastapi_utils.validators import validate_openapi_tags
from red_utils.core import LOG_DIR
from loguru import logger as log


logger_sinks = [
    LoguruSinkStdOut(level=app_settings.log_level).as_dict(),
    LoguruSinkAppFile(sink=f"{LOG_DIR}/api.log").as_dict(),
    LoguruSinkErrFile(sink=f"{LOG_DIR}/api.error.log").as_dict(),
]

allowed_origins = ["*"]
allow_credentials = True
allowed_methods = ["*"]
allowed_headers = ["*"]

app: FastAPI = get_app(
    debug=api_settings.debug,
    cors=True,
    title=api_settings.title,
    description=api_settings.description,
    version=api_settings.version,
    openapi_tags=tags_metadata,
    openapi_url=default_openapi_url,
)

app.include_router(healthcheck.router)
app.router.redirect_slashes = False

if __name__ == "__main__":
    init_logger(sinks=logger_sinks)
    setup_uvicorn_logging(level="DEBUG")

    log.info(f"API start")
