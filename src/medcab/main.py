from __future__ import annotations

from core.dependencies import APP_SETTINGS, ENSURE_DIRS
from domain.product import Product
from domain.purchase import Purchase
from domain.dispensary import Dispensary

from examples.products import load_example_products_simplified

from red_utils.std.path_utils import ensure_dirs_exist
from loguru import logger as log
from red_utils.ext.loguru_utils import LoguruSinkStdOut, init_logger

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
        purchase.dispensary = Dispensary(name="Rise Cannabis", city="Cleveland", state="OH")
        purchase.price = 36.00
        log.debug(f"Purchase: {purchase}")

if __name__ == "__main__":
    init_logger([LoguruSinkStdOut(level=APP_SETTINGS.log_level).as_dict()])
    log.info(f"Settings: {APP_SETTINGS}")

    ensure_dirs_exist(ENSURE_DIRS)
    
    demo()    
