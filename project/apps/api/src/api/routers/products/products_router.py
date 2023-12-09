import json
import uuid

from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from loguru import logger as log

from domain.api.product import Product, ProductUpdate, ProductCreate

from core.config import app_settings, api_settings

tags = ["products"]

router = APIRouter(prefix="/products", tags=tags)


@router.get("/")
def product_index() -> dict[str, str]:
    log.debug(f"/products root reached")
    return {"msg": "Products root reached"}
