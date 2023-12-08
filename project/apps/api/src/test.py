import sys

sys.path.append(".")

from core import app_settings, api_settings

from red_utils.core.constants import DATA_DIR, LOG_DIR, CACHE_DIR, SERIALIZE_DIR
from red_utils.std import path_utils
from red_utils.ext.loguru_utils import init_logger, LoguruSinkStdOut
from loguru import logger as log

from core.validators.product import (
    VALID_FORMS,
    VALID_FAMILIES,
    validate_form,
    validate_family,
)

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
