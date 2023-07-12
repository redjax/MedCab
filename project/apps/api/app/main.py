from __future__ import annotations

import stackprinter

stackprinter.set_excepthook(style="darkbg2")

from pathlib import Path

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from loguru import logger as log
from settings.config import app_settings, logging_settings
from starlette.routing import Match
from utils.diskcache_utils import default_cache_dir
from utils.fastapi_utils import (
    default_api_str,
    default_openapi_url,
    get_app,
    healthcheck,
    logging_dependency,
    tags_metadata,
    update_tags_metadata,
)
from utils.loguru_utils import init_logger

init_logger()

from routers import api_router

allowed_origins: list[str] = ["*"]
allow_credentials: bool = True
allowed_methods: list[str] = ["*"]
allowed_headers: list[str] = ["*"]

included_routers = [healthcheck.router, api_router.router]
log.debug("Creating frontend FastAPI app")

app = get_app(
    cors=True,
    title=app_settings.APP_TITLE,
    description=app_settings.APP_DESCRIPTION,
    version=app_settings.APP_VERSION,
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
    if app_settings.APP_ENV == "dev":
        app.mount("/static", StaticFiles(directory="static/dev"), name="static")
    else:
        app.mount("/static", StaticFiles(directory="static/live"), name="static")

## Include routers
app.include_router(healthcheck.router)
## Include custom logging_dependency as a Depends()
app.include_router(api_router.router, dependencies=[Depends(logging_dependency)])

## Fix links redirecting from /endpoint to //endpoint
app.router.redirect_slashes = False

if __name__ == "__main__":
    log.info("Starting frontend app")

    log.debug(f"App settings: {app_settings}")
