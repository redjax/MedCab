from fastapi import APIRouter, Depends, HTTPException
from loguru import logger as log
from core.config import app_settings
from red_utils.ext.fastapi_utils import default_api_str, tags_metadata

router = APIRouter(
    prefix=default_api_str, responses={404: {"description": "Not found"}}
)

## Include sub-routers
#  router.include_router(xxx_router.router)


@router.get("/")
def router_index() -> dict[str, str]:
    log.debug(f"API router root reached")
    return {"msg": "API root reached"}
