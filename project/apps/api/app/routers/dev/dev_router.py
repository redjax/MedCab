from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from loguru import logger as log
from utils.fastapi_utils import default_api_str, tags_metadata

## Import routers from routers/dev
# from .index import index_router
# from .varieties import varieties_router

router = APIRouter(responses={404: {"description": "Not found"}})

## Add subrouters to dev router
# router.include_router(index_router.router)
# router.include_router(varieties_router.router)
