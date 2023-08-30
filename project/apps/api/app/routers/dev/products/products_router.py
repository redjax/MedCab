"""API Router for Garlic endpoints."""
from __future__ import annotations

import json

from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from loguru import logger as log

from domain.product import Product, ProductUpdate, ProductCreate, crud

from constants import ENV
from dependencies import get_db

tags = ["products"]

router = APIRouter(prefix="/products", tags=tags)


@router.get("/")
def product_index() -> dict[str, str]:
    log.debug("/products root reached")
    return {"msg": "Products root reached"}


@router.post(
    "/create",
    summary="Add new Product to database",
    description="Input a Product, convert to a ProductModel & add to database",
    response_model=Product,
    response_model_exclude_unset=True,
)
def create_product(product: Product, db: crud.Session = Depends(get_db)):
    db_product = crud.create_product(product=product, db=db)

    if not db_product:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "warning": f"Product [{product.name}] already exists in the database"
            },
        )

    return db_product
