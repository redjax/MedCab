from __future__ import annotations

from api.routers.products import products_router

from core.config import app_settings
from fastapi import APIRouter, Depends, HTTPException
from loguru import logger as log
from red_utils.ext.fastapi_utils import default_api_str, tags_metadata

router = APIRouter(
    prefix=default_api_str, responses={404: {"description": "Not found"}}
)

## Include sub-routers
#  router.include_router(xxx_router.router)
router.include_router(products_router.router)


@router.get("/")
def router_index() -> dict[str, str]:
    log.debug(f"API router root reached")
    return {"msg": "API root reached"}
