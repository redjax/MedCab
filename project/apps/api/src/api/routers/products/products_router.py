from __future__ import annotations

import json

from pathlib import Path
import uuid

from core.config import api_settings, app_settings
from core.dependencies import get_db
from domain.api.product import Product, ProductCreate, ProductUpdate, ProductModel, crud

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from loguru import logger as log

tags = ["products"]

router = APIRouter(prefix="/products", tags=tags)


@router.get("/")
def product_index() -> dict[str, str]:
    log.debug(f"/products root reached")
    return {"msg": "Products root reached"}

@router.get("/all", summary="Return all Products from the database.", description="Loads all objects from the database and returns them as a list of JSON objects.", tags=["GET"])
def get_all_products_from_db(db: crud = Depends(get_db)):
    all_products = crud.get_all_products(db=db)
    
    return all_products

@router.get("/count", summary="Get cound of Products in database", description="Deletes ALL Product objects from the database.", tags=["GET"])
def get_count_products_from_db(db: crud.Session = Depends(get_db)):
    product_count: int = crud.count_product(db=db)
    
    if not product_count:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"error": "No Products found in database, or an error occurred"})
    
    return JSONResponse(status_code=status.HTTP_200_OK, content={"count": product_count})

@router.get("/strain/{strain_name}", summary="Retrieve Product by strin name", description="Retrieve Product(s) matching strain value.", tags=["GET"])
def get_product_from_db_by_strain(
    strain_name: str = None, db: crud.Session = Depends(get_db)
):
    db_product = crud.get_product_by_strain(strain_name=strain_name, db=db)

    if not db_product:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "error": f"Product not found by name {strain_name}. Note: Names in the database are case sensitive."
            },
        )

    return db_product


@router.get("/id/{id}", summary="Retrieve Product by id", description="Search and return the database Product matching passed ID.", tags=["GET"])
def get_product_from_db_by_id(id: uuid.UUID = None, db: crud.Session = Depends(get_db)):
    db_product = crud.get_product_by_id(id=id, db=db)

    if not db_product:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "error": f"Product not found by ID: {id}. Note: Names in the database are case sensitive."
            },
        )

    return db_product


@router.get(
    "/family/{family}", summary="Retrieve Products by family (indica, sativa, hybrid)", tags=["GET"]
)
def get_products_from_db_by_strain(family: str, db: crud.Session = Depends(get_db)):
    db_products = crud.get_products_by_family(family=family, db=db)

    if not db_products:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": f"Could not find any Products by strain: {family}"},
        )

    return db_products


@router.get("/form/{form}", summary="Retrieve Products by form", tags=["GET"])
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
    description="Input a Product, convert to a ProductModel & add to database.",
    response_model=Product,
    response_model_exclude_unset=True,tags=["POST"]
)
def create_product_in_db(product: Product, db: crud.Session = Depends(get_db)):
    try:
        db_product = crud.create_product(product=product, db=db)
    except Exception as exc:
        raise Exception(f"Unhandled exception creating Product '{product.strain}. Details: {exc}")

    if not db_product:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "warning": f"Product [{product.strain}] already exists in the database"
            },
        )

    return db_product


@router.post("/update/id/{id}", summary="Update a Product by ID", tags=["POST"])
def update_product_in_db_by_id(
    id: uuid.UUID = None, product: Product = None, db: crud.Session = Depends(get_db)
):
    db_product_update = crud.update_product_by_id(id=id, product=product, db=db)

    if not db_product_update:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": f"Product not found by ID: {id}"},
        )

    return db_product_update


# @router.post("/update/strain/{strain_name}", summary="Update a Product by strain name", tags=["POST"])
# def update_product_in_db_by_name(
#     strain_name: str = None, product: Product = None, db: crud.Session = Depends(get_db)
# ):
#     db_product_update = crud.update_product_by_strain(
#         strain_name=strain_name, product=product, db=db
#     )

#     if not db_product_update:
#         return JSONResponse(
#             status_code=status.HTTP_404_NOT_FOUND,
#             content={"error": f"Product not found by name: {strain_name}"},
#         )

#     return db_product_update


@router.delete("/id/{id}", summary="Delete a Product by ID", description="Search database for Product matching passed ID and delete it.", tags=["DELETE"])
def delete_product_from_db_by_id(id: uuid.UUID, db: crud.Session = Depends(get_db)):
    _deleted = crud.delete_product_by_id(id=id, db=db)

    if not _deleted:
        return JSONResponse(status_code=404, content=f"No Product exists with ID: {id}")

    return JSONResponse(status_code=202, content=f"Deleted Product with ID: {id}")


if not app_settings.env == "prod":
    @router.delete("/all", summary="Delete all Products", description="Deletes all Product objects from the database. Use with caution. This endpoint is disabled if the app is running in 'prod' mode.", tags=["DELETE"])
    def delete_all_products_from_db(db: crud.Session = Depends(get_db)):
        _deleted = crud.delete_all_products(db=db)

        if not _deleted:
            return JSONResponse(
                status_code=404, content=f"No Products exist in the database"
            )

        return JSONResponse(
            status_code=202,
            content=f"Deleted all Products. Number of deleted records: {len(_deleted)}",
        )
