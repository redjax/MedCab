from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from loguru import logger as log
from settings.config import app_settings
from utils.fastapi_utils import default_api_str, tags_metadata

ENV: str = app_settings.APP_ENV

if ENV == "dev":
    log.debug(f"Building dev router")
    from routers.dev import dev_router

elif ENV == "prod":
    log.debug(f"Building prod router")
    from routers.prod import prod_router

else:
    log.warning(
        ValueError(f"Invalid env: {app_settings.APP_ENV}. Defaulting to 'prod'")
    )
    ENV: str = "prod"

    from routers.prod import prod_router


router = APIRouter(responses={404: {"description": "Not found"}})

## Include sub-routers
#  router.include_router(xxx_router.router)
if ENV == "dev":
    router.include_router(dev_router.router)
else:
    router.include_router(prod_router.router)

log.debug(f"API router included routers: {router.routes}")


@router.get("/")
def router_index() -> dict[str, str]:
    log.debug(f"API Router index reached.")
    return {"msg": "Root page reached."}
