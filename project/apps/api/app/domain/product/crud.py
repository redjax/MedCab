import uuid

from .schemas import ProductCreate, Product
from .models import ProductModel

from sqlalchemy.orm import Session, Query

from constants import valid_strains, valid_forms

from loguru import logger as log

from lib.parse_schema import parse_pydantic_schema


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


def create_product(product: ProductCreate = None, db: Session = None) -> ProductModel:
    validate_db(db)

    log.debug(f"Product ({type(product)}): {product}")

    try:
        with db as sess:
            db_product: Query = (
                sess.query(ProductModel)
                .where(ProductModel.name == product.name)
                .first()
            )

            if db_product:
                return False
            else:
                dump_schema = parse_pydantic_schema(schema=product)

                new_product: ProductModel = ProductModel(**dump_schema)

                sess.add(new_product)
                sess.commit()

                return new_product

    except Exception as exc:
        raise Exception(f"Unhandled exception creating Product. Details: {exc}")


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


def get_product_by_name(name: str = None, db: Session = None) -> ProductModel:
    if not name:
        raise ValueError("Missing a name to search")

    if not isinstance(name, str):
        raise ValueError(f"Invalid type for name: {type(name)}. Must be of type str")

    try:
        with db as sess:
            db_product = (
                sess.query(ProductModel).where(ProductModel.name == name).first()
            )

            return db_product

    except Exception as exc:
        raise Exception(
            f"Unhandled exception retrieving Product by name '{name}'. Details: {exc}"
        )


def get_products_by_strain(
    strain: str = None, db: Session = None
) -> list[ProductModel]:
    if not strain:
        raise ValueError(f"Missing strain")

    if not strain in valid_strains:
        raise ValueError(f"Invalid strain: {strain}. Must be one of: {valid_strains}")

    try:
        with db as sess:
            db_products: list[ProductModel] = (
                sess.query(ProductModel).where(ProductModel.strain == strain).all()
            )

            return db_products

    except Exception as exc:
        raise Exception(
            f"Unhandled exception getting Products by strain. Details: {exc}"
        )


def get_products_by_form(form: str = None, db: Session = None) -> list[ProductModel]:
    if not form:
        raise ValueError(f"Missing form")

    if not form in valid_forms:
        raise ValueError(f"Invalid form: {form}. Must be one of: {valid_forms}")

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


def update_product_by_name(
    name: str = None, product: Product = None, db: Session = None
):
    try:
        with db as sess:
            db_product: Query = (
                sess.query(ProductModel).filter(ProductModel.name == name).first()
            )

            if not db_product:
                return None

            update_data = product.model_dump(exclude_unset=True)

            sess.query(ProductModel).filter(ProductModel.name == name).update(
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
