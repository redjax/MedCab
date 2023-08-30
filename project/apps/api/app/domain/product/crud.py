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
