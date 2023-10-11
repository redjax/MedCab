import uuid

from medcab_backend.domain.product.models import ProductModel
from medcab_backend.domain.product.schemas import Product, ProductCreate
from medcab_backend.domain.product.validators import valid_families, valid_forms
from red_utils.ext.sqlalchemy_utils import get_session
from red_utils.ext.pydantic_utils import parse_pydantic_schema
from medcab_backend.dependencies import engine

from loguru import logger as log

import sqlalchemy as sa
from sqlalchemy.orm import Session, Query, sessionmaker
from sqlalchemy import func, select

SessionLocal = get_session(engine=engine)


def validate_db(db: Session = None) -> Session:
    if not db:
        raise ValueError("Missing DB Session object")

    return db


def count_product(db: sessionmaker[Session] = SessionLocal) -> int:
    try:
        with db() as sess:
            product_count = sess.query(func.count(ProductModel.id)).scalar()

            return product_count
    except Exception as exc:
        log.error(
            f"Unhandled exception getting count of Products in database. Details: {exc}"
        )
        return None


def create_product(
    product: ProductCreate = None, db: sessionmaker[Session] = SessionLocal
) -> ProductModel:
    """Create a new Product in the database."""
    validate_db(db)

    log.debug(f"Product ({type(product)}): {product}")

    try:
        with db() as sess:
            db_product: ProductModel | None = None

            log.debug(f"Building SELECT statement on .strain")
            db_product_sel = select(ProductModel).where(
                ProductModel.strain == product.strain
            )
            log.debug("Executing SELECT ProductModel statement")

            db_products: list[ProductModel] = sess.execute(db_product_sel).all()
            log.debug(
                f"Results: ({type(db_products)}) [items:{len(db_products)}]: {db_products}"
            )

            if db_products is None:
                log.warning(
                    f"No matching strain found for '{product.strain}'. Creating."
                )

                dump_schema = parse_pydantic_schema(schema=product)
                new_product: ProductModel = ProductModel(**dump_schema)

                try:
                    sess.add(new_product)
                    sess.commit()

                    return new_product
                except Exception as exc:
                    raise Exception(
                        f"Unhandled exception writing new ProductModel to database. Details: {exc}"
                    )

            else:
                log.debug(
                    f"Found [{len(db_products)}] products with strain name: {product.strain}"
                )

                for p in db_products:
                    if not p.form == p.form:
                        pass
                    else:
                        log.debug(
                            f"Product [{product.strain}] in form {product.form} already exists."
                        )

                        db_product: ProductModel = p

                        return db_product

                if db_product is None:
                    log.debug(
                        f"Product [{product.strain}] in form {product.form} not found in database. Creating"
                    )

                    dump_schema = parse_pydantic_schema(schema=product)

                    new_product: ProductModel = ProductModel(**dump_schema)

                    try:
                        sess.add(new_product)
                        sess.commit()

                        return new_product
                    except Exception as exc:
                        raise Exception(
                            f"Unhandled exception creating new Product. Details: {exc}"
                        )

                else:
                    return db_product

    except Exception as exc:
        raise Exception(f"Unhandled exception creating Product. Details: {exc}")


def get_all_products(db: sessionmaker[Session] = SessionLocal) -> list[ProductModel]:
    """Return all products from the databas."""
    validate_db(db)

    try:
        with db() as sess:
            all_products = sess.query(ProductModel).all()

            return all_products

    except Exception as exc:
        raise Exception(f"Unhandled exception getting all Products. Details: {exc}")


def get_product_by_id(
    id: uuid.UUID = None, db: sessionmaker[Session] = None
) -> ProductModel:
    try:
        with db() as sess:
            db_product = sess.query(ProductModel).filter(ProductModel.id == id).first()

        return db_product

    except Exception as exc:
        raise Exception(
            f"Unhandled exception retrieving Product by ID: '{id}'. Details: {exc}"
        )


def get_product_by_strain(
    strain_name: str = None, db: sessionmaker[Session] = SessionLocal
) -> ProductModel:
    if not strain_name:
        raise ValueError("Missing a name to search")

    if not isinstance(strain_name, str):
        raise ValueError(
            f"Invalid type for name: {type(strain_name)}. Must be of type str"
        )

    try:
        with db() as sess:
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
    family: str = None, db: sessionmaker[Session] = SessionLocal
) -> list[ProductModel]:
    if not family:
        raise ValueError(f"Missing strain")

    if not family in valid_families:
        raise ValueError(f"Invalid strain: {family}. Must be one of: {valid_families}")

    try:
        with db() as sess:
            db_products: list[ProductModel] = (
                sess.query(ProductModel).where(ProductModel.family == family).all()
            )

            return db_products

    except Exception as exc:
        raise Exception(
            f"Unhandled exception getting Products by strain. Details: {exc}"
        )


def get_products_by_form(
    form: str = None, db: sessionmaker[Session] = SessionLocal
) -> list[ProductModel]:
    if not form:
        raise ValueError(f"Missing form")

    if not form in valid_forms:
        raise ValueError(f"Invalid form: {form}. Must be one of: {valid_forms}")

    try:
        with db() as sess:
            db_products: list[ProductModel] = (
                sess.query(ProductModel).where(ProductModel.form == form).all()
            )

            return db_products

    except Exception as exc:
        raise Exception(f"Unhandled exception getting Products by form. Details: {exc}")


def update_product_by_id(
    id: uuid.UUID = None,
    product: Product = None,
    db: sessionmaker[Session] = SessionLocal,
):
    try:
        with db() as sess:
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
    strain_name: str = None,
    product: Product = None,
    db: sessionmaker[Session] = SessionLocal,
):
    try:
        with db() as sess:
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


def delete_product_by_id(
    id: uuid.UUID = None, db: sessionmaker[Session] = SessionLocal
):
    try:
        with db() as sess:
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


def delete_all_products(db: sessionmaker[Session] = SessionLocal):
    try:
        with db() as sess:
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
