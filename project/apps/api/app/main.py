from __future__ import annotations

import stackprinter

stackprinter.set_excepthook(style="darkbg2")

from pathlib import Path

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from loguru import logger as log

# from settings.config import app_settings, logging_settings
from config import settings
from starlette.routing import Match

from red_utils.diskcache_utils import default_cache_dir
from red_utils.fastapi_utils import (
    default_api_str,
    default_openapi_url,
    get_app,
    healthcheck,
    logging_dependency,
    tags_metadata,
    update_tags_metadata,
    validate_openapi_tags,
    fix_api_docs,
)
from red_utils.loguru_utils import init_logger

from constants import (
    ENV,
    CONTAINER_ENV,
    env_string,
    app_title,
    app_description,
    app_version,
)

from dependencies import Base, create_base_metadata, engine, db_config

from domain.product import ProductModel

init_logger()

from routers import api_router

create_base_metadata(Base(), engine=engine)

allowed_origins: list[str] = ["*"]
allow_credentials: bool = True
allowed_methods: list[str] = ["*"]
allowed_headers: list[str] = ["*"]

included_routers = [healthcheck.router, api_router.router]
log.debug("Creating frontend FastAPI app")

app: FastAPI = get_app(
    cors=True,
    title=app_title,
    description=app_description,
    version=app_version,
    openapi_tags=tags_metadata,
    openapi_url=default_openapi_url,
    debug=True,
    # routers=included_routers,
)

## Mount directories
if not Path("static").exists():
    log.debug("Static path does not exist, skip mounting")
else:
    log.debug("Found /static dir, mounting to app")
    if settings.env == "dev":
        app.mount("/static", StaticFiles(directory="static/dev"), name="static")
    else:
        app.mount("/static", StaticFiles(directory="static/prod"), name="static")

## Include routers
app.include_router(healthcheck.router)
## Include custom logging_dependency as a Depends()
app.include_router(api_router.router, dependencies=[Depends(logging_dependency)])

## Fix links redirecting from /endpoint to //endpoint
app.router.redirect_slashes = False

if __name__ == "__main__":
    log.info("Starting frontend app")
    log.debug(f"App settings: {settings.__dict__}")
