from __future__ import annotations

import uuid

from .models import ProductModel
from .schemas import Product, ProductCreate

from core.utils.crud_utils import convert_sqla_rows_to_dicts
from core.validators.product import VALID_FAMILIES, VALID_FORMS
from loguru import logger as log
from red_utils.ext.pydantic_utils.parsers import parse_pydantic_schema
from sqlalchemy import func, select
from sqlalchemy.engine import Row
from sqlalchemy.orm import Query, Session

def validate_db(db: Session = None) -> Session:
    if not db:
        raise ValueError("Missing DB Session object")

    if not isinstance(db, Session):
        raise TypeError(
            f"Invalid type for db: ({type(db)}). Must be of type sqlalchemy.orm.Session"
        )

    return db


def validate_product_create(product) -> ProductCreate:
    if not product:
        raise ValueError("Missing Product to add to database")

    if not isinstance(product, ProductCreate):
        raise TypeError(
            f"Invalid type for Product: ({type(product)}). Must be of type ProductCreate"
        )

    return product


def count_product(db: Session = None) -> int:
    try:
        with db as sess:
            product_count = sess.query(func.count(ProductModel.id)).scalar()

            return product_count
    except Exception as exc:
        log.error(
            f"Unhandled exception getting count of Products in database. Details: {exc}"
        )
        return None


def create_product(product: ProductCreate = None, db: Session = None) -> ProductModel:
    validate_db(db)

    log.debug(f"Product ({type(product)}): {product}")

    with db as sess:
        db_product: ProductModel | None = None

        log.debug(f"Building SELECT statement on .strain")
        try:
            db_product_sel = select(ProductModel).where(
                ProductModel.strain == product.strain
            )
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception building SELECT Product [{product.strain}] statement. Details: {exc}"
            )
            log.error(msg)

        log.debug(f"Executing SELECT ProductModel statement")

        try:
            db_products: list[Row] = sess.execute(db_product_sel).all()

        except Exception as exc:
            msg = Exception(
                f"Unhandled exception executing SELECT statement for Product [{product.strain}]. Details: {exc}"
            )
            log.error(msg)

            raise msg

        if db_products is not None:
            log.debug(
                f"Results: ({type(db_products)}) [items:{len(db_products)}]: {db_products}"
            )

        if db_products is None:
            log.debug(f"No matching strain found for '{product.strain}. Creating.")

            try:
                dump_schema = parse_pydantic_schema(schema=product)
            except Exception as exc:
                msg = Exception(
                    f"Unhandled exception dumping Pydantic schema. Details: {exc}"
                )
                log.error(msg)

            log.debug(f"Dump schema ({type(dump_schema)}): {dump_schema}")

            try:
                new_product: ProductModel = ProductModel(**dump_schema)
            except Exception as exc:
                msg = Exception(
                    f"Unhandled exception convering Product schema to model. Schema ({type(dump_schema)}): {dump_schema}. Details: {exc}"
                )

            try:
                sess.add(new_product)
                sess.commit()

                return new_product

            except Exception as exc:
                msg = Exception(
                    f"Unhandled exception committing Product to database. Details: {exc}"
                )

        else:
            log.debug(
                f"Found [{len(db_products)}] Product(s) matching strain {product.strain} in the database."
            )
            db_product_dicts: list[dict] = convert_sqla_rows_to_dicts(rows=db_products)

            log.debug(f"Converted [{len(db_product_dicts)}] Product Row(s) to dict(s)")

            for _product in db_product_dicts:
                p: ProductModel = _product["ProductModel"]
                log.debug(f"_product ({type(p)}): {p}")
                # log.debug(f"Product:\n\tStrain: {p.strain}\n\tFamily: {p.family}\n\tForm: {p.form}")

                if not p.form == product.form:
                    pass
                else:
                    log.debug(
                        f"Product [{product.strain}] in form {product.form} already exists"
                    )

                    db_product: ProductModel = p

            if db_product is None:
                log.debug(
                    f"Product [{product.strain}] in form {product.form} not found in database. Creating."
                )

                try:
                    dump_schema = parse_pydantic_schema(schema=product)
                except Exception as exc:
                    msg = Exception(
                        f"Unhandled exception dumping Product schema to dict. Product ({type(product)}): {product}. Details: {exc}"
                    )
                    log.error(msg)

                try:
                    new_product: ProductModel = ProductModel(**dump_schema)
                except Exception as exc:
                    msg = Exception(
                        f"Unhandled exception converting Product schema to model. Schema ({type(dump_schema)}): {dump_schema}. Details: {exc}"
                    )

                try:
                    sess.add(new_product)
                    sess.commit()

                    return new_product

                except Exception as exc:
                    msg = Exception(
                        f"Unhandled exception inserting new Product. Product ({type(new_product)}): {new_product}. Details: {exc}"
                    )

            else:
                return db_product


def get_all_products(db: Session = None) -> list[ProductModel]:
    validate_db(db)

    try:
        with db as sess:
            all_products = sess.query(ProductModel).all()

            return all_products

    except Exception as exc:
        raise Exception(f"Unhandled exception getting all Products. Details: {exc}")


def get_product_by_id(id: uuid.UUID = None, db: Session = None) -> ProductModel:
    try:
        with db as sess:
            db_product = sess.query(ProductModel).filter(ProductModel.id == id).first()

        return db_product

    except Exception as exc:
        raise Exception(
            f"Unhandled exception retrieving Product by ID: '{id}'. Details: {exc}"
        )


def get_product_by_strain(strain_name: str = None, db: Session = None) -> ProductModel:
    if not strain_name:
        raise ValueError("Missing a name to search")

    if not isinstance(strain_name, str):
        raise ValueError(
            f"Invalid type for name: {type(strain_name)}. Must be of type str"
        )

    try:
        with db as sess:
            db_product = (
                sess.query(ProductModel)
                .where(ProductModel.strain == strain_name)
                .first()
            )

            return db_product

    except Exception as exc:
        raise Exception(
            f"Unhandled exception retrieving Product by name '{strain_name}'. Details: {exc}"
        )


def get_products_by_family(
    family: str = None, db: Session = None
) -> list[ProductModel]:
    if not family:
        raise ValueError(f"Missing strain")

    if family not in VALID_FAMILIES:
        raise ValueError(f"Invalid strain: {family}. Must be one of: {VALID_FAMILIES}")

    try:
        with db as sess:
            db_products: list[ProductModel] = (
                sess.query(ProductModel).where(ProductModel.family == family).all()
            )

            return db_products

    except Exception as exc:
        raise Exception(
            f"Unhandled exception getting Products by strain. Details: {exc}"
        )


def get_products_by_form(form: str = None, db: Session = None) -> list[ProductModel]:
    if not form:
        raise ValueError(f"Missing form")

    if form not in VALID_FORMS:
        raise ValueError(f"Invalid form: {form}. Must be one of: {VALID_FORMS}")

    try:
        with db as sess:
            db_products: list[ProductModel] = (
                sess.query(ProductModel).where(ProductModel.form == form).all()
            )

            return db_products

    except Exception as exc:
        raise Exception(f"Unhandled exception getting Products by form. Details: {exc}")


def update_product_by_id(
    id: uuid.UUID = None, product: Product = None, db: Session = None
):
    try:
        with db as sess:
            db_product: Query = (
                sess.query(ProductModel).filter(ProductModel.id == id).first()
            )

            if not db_product:
                return None

            update_data = product.model_dump(exclude_unset=True)

            sess.query(ProductModel).filter(ProductModel.id == id).update(
                update_data, synchronize_session=False
            )

            sess.commit()
            sess.refresh(db_product)

        return db_product

    except Exception as exc:
        raise Exception(f"Unhandled exception updating Product by ID. Details: {exc}")


def update_product_by_strain(
    strain_name: str = None, product: Product = None, db: Session = None
):
    try:
        with db as sess:
            db_product: Query = (
                sess.query(ProductModel)
                .filter(ProductModel.strain == strain_name)
                .first()
            )

            if not db_product:
                return None

            update_data = product.model_dump(exclude_unset=True)

            sess.query(ProductModel).filter(ProductModel.strain == strain_name).update(
                update_data, synchronize_session=False
            )

            sess.commit()
            sess.refresh(db_product)

        return db_product

    except Exception as exc:
        raise Exception(f"Unhandled exception updating Product by ID. Details: {exc}")


def delete_product_by_id(id: uuid.UUID = None, db: Session = None):
    try:
        with db as sess:
            db_product = sess.query(ProductModel).filter(ProductModel.id == id).first()

            if not db_product:
                return None

            log.debug(f"Found Product by ID: {id} - {db_product}. Deleting")

            _del = sess.query(ProductModel).filter(ProductModel.id == id).delete()

            sess.commit()

            return {"success": f"Deleted Product with ID: {id}"}

    except Exception as exc:
        raise Exception(
            f"Unhandled exception deleting Product with ID: {id}. Details: {exc}"
        )


def delete_all_products(db: Session = None):
    try:
        with db as sess:
            db_products = sess.query(ProductModel).all()

            if not db_products:
                log.warning(f"No products in the database")

                return False

            for product in db_products:
                sess.delete(product)

            sess.commit()

            return db_products

    except Exception as exc:
        log.error(f"Unhandled exception deleting all Products. Details: {exc}")
        return False
