from __future__ import annotations

from pathlib import Path

from core.dependencies import APP_SETTINGS, ENSURE_DIRS
from loguru import logger as log
from red_utils.std.path_utils import ensure_dirs_exist

def entrypoint_app_startup(ensure_dirs: list[Path] = ENSURE_DIRS):
    log.info(f"Entrypoint: app_startup")
    ensure_dirs_exist(dirs=ensure_dirs)
