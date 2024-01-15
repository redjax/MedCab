from __future__ import annotations

from core.db import get_db_session
from core.dependencies import APP_SETTINGS, DB_SETTINGS, ENSURE_DIRS
from domain.dispensary import Dispensary
from domain.product import Product, ProductModel
from domain.purchase import Purchase, PurchaseNote
from entrypoints.startup import entrypoint_sqlalchemy_startup
from examples.products import load_example_products_simplified
from loguru import logger as log
from red_utils.ext.loguru_utils import LoguruSinkStdOut, init_logger
from red_utils.ext.sqlalchemy_utils import (
    create_base_metadata,
    generate_metadata,
    get_engine,
    get_session,
    saSQLiteConnection,
)
from red_utils.std.path_utils import ensure_dirs_exist

def demo():
    ex_products = load_example_products_simplified()
    log.debug(f"Example Products: {ex_products}")

    products: list[Product] = []

    for p in ex_products:
        product: Product = Product.model_validate(p)
        products.append(product)

    for p in products:
        log.debug(f"Product ({type(p)}): {p}")
        purchase: Purchase = Purchase(date="2024-01-13", product=p)
        purchase.dispensary = Dispensary(
            name="Rise Cannabis", city="Cleveland", state="OH"
        )
        purchase.price = 36.00
        log.debug(f"Purchase: {purchase}")


if __name__ == "__main__":
    init_logger([LoguruSinkStdOut(level=APP_SETTINGS.log_level).as_dict()])
    log.info(f"Settings: {APP_SETTINGS}")
    log.info(f"DB Settings: {DB_SETTINGS}")

    ensure_dirs_exist(ENSURE_DIRS)

    entrypoint_sqlalchemy_startup()
