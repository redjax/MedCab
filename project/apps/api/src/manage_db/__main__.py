import sys
sys.path.append(".")

from manage_db import insert_samples, API, EXAMPLE_SCHEMAS_DIR, EXAMPLE_PRODUCTS_DIR, EXAMPLE_SIMPLIFIED_PRODUCTS_DIR
from core.config import app_settings

from red_utils.ext.loguru_utils import init_logger, LoguruSinkStdOut
from loguru import logger as log

if __name__ == "__main__":
    init_logger([LoguruSinkStdOut(level=app_settings.log_level).as_dict()])


    log.info(f"[env:{app_settings.env}|container:{app_settings.container_env}] App Start")
    insert_samples(api=API, products_json_dir=EXAMPLE_SIMPLIFIED_PRODUCTS_DIR)