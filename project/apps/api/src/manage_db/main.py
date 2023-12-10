import sys
sys.path.append(".")

from pathlib import Path

from .schemas import APIServer
from .operations import test_connection, remove_all_items, insert_product_into_db, insert_samples, loop_insert_products

from core.constants import DATA_DIR
from core.config import app_settings, api_settings

from loguru import logger as log

from red_utils.ext.loguru_utils import init_logger, LoguruSinkStdOut


if __name__ == "__main__":
    init_logger([LoguruSinkStdOut(level=app_settings.log_level).as_dict()])

EXAMPLE_SCHEMAS_DIR: Path = Path(f"{DATA_DIR}/example_schemas")
EXAMPLE_PRODUCTS_DIR: Path = Path(f"{EXAMPLE_SCHEMAS_DIR}/products")
EXAMPLE_SIMPLIFIED_PRODUCTS_DIR: Path = Path(f"{EXAMPLE_PRODUCTS_DIR}/simplified_for_testing")

API: APIServer = APIServer()


def main(api: APIServer = API):
    log.info(f"[env:{app_settings.env}|container:{app_settings.container_env}] App Start")
    insert_samples()
    remove_all_items(api=api)

    

if __name__ == "__main__":
    log.debug(f"API URL string: {API.base_url}")
    
    main(api=API)