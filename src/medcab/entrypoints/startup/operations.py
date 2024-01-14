from __future__ import annotations

from pathlib import Path

from core.dependencies import APP_SETTINGS, ENSURE_DIRS
from loguru import logger as log
from red_utils.ext.loguru_utils import LoguruSinkStdOut, init_logger
from red_utils.std.path_utils import ensure_dirs_exist

if __name__ == "__main__":
    init_logger([LoguruSinkStdOut(level=APP_SETTINGS.log_level).as_dict()])


def entrypoint_app_startup(ensure_dirs: list[Path] = ENSURE_DIRS):
    log.info(f"Entrypoint: app_startup")

    log.info("Running app startup operations")
    try:
        ensure_dirs_exist(ensure_dirs)
        log.success("App startup complete")
    except Exception as exc:
        msg = Exception(f"Unhandled exception running app startup. Details: {exc}")
        log.error(msg)

        raise msg
