from __future__ import annotations

import sys

sys.path.append(".")

from core import api_settings, app_settings
from core.validators.product import (
    VALID_FAMILIES,
    VALID_FORMS,
    validate_family,
    validate_form,
)
from loguru import logger as log
from red_utils.core.constants import CACHE_DIR, DATA_DIR, LOG_DIR, SERIALIZE_DIR
from red_utils.ext.loguru_utils import LoguruSinkStdOut, init_logger
from red_utils.std import path_utils

if __name__ == "__main__":
    init_logger(sinks=[LoguruSinkStdOut(level=app_settings.log_level).as_dict()])
    path_utils.ensure_dirs_exist(
        ensure_dirs=[DATA_DIR, LOG_DIR, CACHE_DIR, SERIALIZE_DIR]
    )
    log.info(
        f"[env:{app_settings.env}|container:{app_settings.container_env}] App Start"
    )
    log.debug(f"App Settings: {app_settings}")
    log.debug(f"API Settings: {api_settings}")
