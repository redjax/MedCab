from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from loguru import logger as log
from red_utils.fastapi_utils import default_api_str, tags_metadata

## Import routers from routers/dev
from .products import products_router

router = APIRouter(responses={404: {"description": "Not found"}})

## Add subrouters to dev router
router.include_router(products_router.router)
