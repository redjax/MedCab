from __future__ import annotations

import sys

sys.path.append(".")

from pathlib import Path

from api.routers import api_router

from core import api_settings, app_settings
from core.api import CUSTOM_TAGS
from core.dependencies import Base, create_base_metadata, engine, db_config

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from loguru import logger as log

from red_utils.core import LOG_DIR
from red_utils.ext.fastapi_utils import (
    default_api_str,
    default_openapi_url,
    fix_api_docs,
    get_app,
    healthcheck,
    logging_dependency,
    setup_uvicorn_logging,
    tags_metadata,
    update_tags_metadata,
)
from red_utils.ext.fastapi_utils.validators import validate_openapi_tags
from red_utils.ext.loguru_utils import (
    LoguruSinkAppFile,
    LoguruSinkErrFile,
    LoguruSinkStdOut,
    init_logger,
)

from domain.api.product import ProductModel

logger_sinks = [
    LoguruSinkStdOut(level=app_settings.log_level).as_dict(),
    LoguruSinkAppFile(sink=f"{LOG_DIR}/api.log").as_dict(),
    LoguruSinkErrFile(sink=f"{LOG_DIR}/api.error.log").as_dict(),
]

allowed_origins = ["*"]
allow_credentials = True
allowed_methods = ["*"]
allowed_headers = ["*"]

update_tags_metadata(tags_metadata=tags_metadata, update_metadata=CUSTOM_TAGS)

create_base_metadata(Base(), engine=engine)

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
app.include_router(api_router.router)

app.router.redirect_slashes = False

if __name__ == "__main__":
    init_logger(sinks=logger_sinks)
    setup_uvicorn_logging(level="DEBUG")

    log.info(f"API start")
