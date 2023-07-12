"""API Router for Garlic endpoints."""
from __future__ import annotations

import json

from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from loguru import logger as log


tags = ["products"]

router = APIRouter(prefix="/products", tags=tags)


@router.get("/")
def product_index() -> dict[str, str]:
    log.debug("/product root reached")
    return {"msg": "Product root reached"}
