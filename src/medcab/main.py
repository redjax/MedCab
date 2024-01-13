from __future__ import annotations

from core.dependencies import APP_SETTINGS, ENSURE_DIRS
from entrypoints.startup import entrypoint_app_startup

from loguru import logger as log
from red_utils.ext.loguru_utils import LoguruSinkStdOut, init_logger

if __name__ == "__main__":
    init_logger([LoguruSinkStdOut(level=APP_SETTINGS.log_level).as_dict()])
    log.info(f"Settings: {APP_SETTINGS}")
    
    entrypoint_app_startup()
