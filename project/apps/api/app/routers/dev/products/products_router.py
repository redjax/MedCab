"""API Router for Garlic endpoints."""
from __future__ import annotations

import json

from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from loguru import logger as log

from domain.product import Product, ProductUpdate, ProductCreate, crud, ProductModel

from constants import ENV
from dependencies import get_db

tags = ["products"]

router = APIRouter(prefix="/products", tags=tags)


@router.get("/")
def product_index() -> dict[str, str]:
    log.debug("/products root reached")
    return {"msg": "Products root reached"}


@router.get(
    "/all",
    summary="Return all Products from the database.",
)
def get_all_products_from_db(db: crud.Session = Depends(get_db)):
    """Return all Products from DB."""
    all_products = crud.get_all_products(db=db)

    return all_products


@router.get("/name/{name}", summary="Retrieve Product by name")
def get_product_from_db_by_name(name: str = None, db: crud.Session = Depends(get_db)):
    # name: str = name.title()

    db_product = crud.get_product_by_name(name=name, db=db)

    if not db_product:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "error": f"Product not found by name {name}. Note: Names in the database are case sensitive."
            },
        )

    return db_product


@router.get("/id/{id}", summary="Retrieve Product by id")
def get_product_from_db_by_id(id: int = None, db: crud.Session = Depends(get_db)):
    db_product = crud.get_product_by_id(id=id, db=db)

    if not db_product:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "error": f"Product not found by ID: {id}. Note: Names in the database are case sensitive."
            },
        )

    return db_product


@router.get("/strain/{strain}", summary="Retrieve Products by strain")
def get_products_from_db_by_strain(strain: str, db: crud.Session = Depends(get_db)):
    db_products = crud.get_products_by_strain(strain=strain, db=db)

    if not db_products:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": f"Could not find any Products by strain: {strain}"},
        )

    return db_products


@router.get("/form/{form}", summary="Retrieve Products by form")
def get_products_from_db_by_form(form: str, db: crud.Session = Depends(get_db)):
    db_products = crud.get_products_by_form(form=form, db=db)

    if not db_products:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": f"Could not find any Products by form: {form}"},
        )

    return db_products


@router.post(
    "/create",
    summary="Add new Product to database",
    description="Input a Product, convert to a ProductModel & add to database",
    response_model=Product,
    response_model_exclude_unset=True,
)
def create_product_in_db(product: Product, db: crud.Session = Depends(get_db)):
    db_product = crud.create_product(product=product, db=db)

    if not db_product:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "warning": f"Product [{product.name}] already exists in the database"
            },
        )

    return db_product


@router.post("/update/id/{id}", summary="Update a Product by ID")
def update_product_in_db_by_id(
    id: int = None, product: Product = None, db: crud.Session = Depends(get_db)
):
    db_product_update = crud.update_product_by_id(id=id, product=product, db=db)

    if not db_product_update:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": f"Product not found by ID: {id}"},
        )

    return db_product_update


@router.post("/update/name/{name}", summary="Update a Product by name")
def update_product_in_db_by_name(
    name: str = None, product: Product = None, db: crud.Session = Depends(get_db)
):
    db_product_update = crud.update_product_by_name(name=name, product=product, db=db)

    if not db_product_update:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": f"Product not found by name: {name}"},
        )

    return db_product_update


@router.delete("/id/{id}", summary="Delete a Product by ID")
def delete_product_from_db_by_id(id: int, db: crud.Session = Depends(get_db)):
    _deleted = crud.delete_product_by_id(id=id, db=db)

    if not _deleted:
        return JSONResponse(status_code=404, content=f"No Product exists with ID: {id}")

    return JSONResponse(status_code=202, content=f"Deleted Product with ID: {id}")
