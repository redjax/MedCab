from __future__ import annotations

from core.dependencies import APP_SETTINGS, ENSURE_DIRS
from examples.products import load_example_products_simplified

from red_utils.std.path_utils import ensure_dirs_exist
from loguru import logger as log
from red_utils.ext.loguru_utils import LoguruSinkStdOut, init_logger

if __name__ == "__main__":
    init_logger([LoguruSinkStdOut(level=APP_SETTINGS.log_level).as_dict()])
    log.info(f"Settings: {APP_SETTINGS}")

    ensure_dirs_exist(ENSURE_DIRS)
    
    ex_products = load_example_products_simplified()
    log.debug(f"Example Products: {ex_products}")
