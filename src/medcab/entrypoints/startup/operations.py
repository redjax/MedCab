from pathlib import Path

from core.dependencies import APP_SETTINGS, ENSURE_DIRS
from red_utils.std.path_utils import ensure_dirs_exist

from loguru import logger as log

def entrypoint_app_startup(ensure_dirs: list[Path] = ENSURE_DIRS):
    log.info(f"Entrypoint: app_startup")
    ensure_dirs_exist(dirs=ensure_dirs)