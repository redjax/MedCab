from .schemas import ProductCreate, Product
from .models import ProductModel

from sqlalchemy.orm import Session

from loguru import logger as log


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


def create_product(product: ProductCreate = None, db: Session = None):
    validate_db(db)

    log.debug(f"Product ({type(product)}): {product}")

    try:
        with db as sess:
            db_product = (
                sess.query(ProductModel)
                .where(ProductModel.name == product.name)
                .first()
            )

            if db_product:
                return False
            else:
                dump_schema: dict = product.model_dump()
                log.debug(f"Schema dump ({type(dump_schema)}): {dump_schema}")

                new_product = ProductModel(**dump_schema)

                sess.add(new_product)
                sess.commit()

                return new_product

    except Exception as exc:
        raise Exception(f"Unhandled exception creating Product. Details: {exc}")


def get_all_products(db: Session = None):
    validate_db(db)

    try:
        with db as sess:
            all_products = sess.query(ProductModel).all()

            return all_products

    except Exception as exc:
        raise Exception(f"Unhandled exception getting all Products. Details: {exc}")


def get_product_by_name(name: str = None, db: Session = None) -> Product:
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
