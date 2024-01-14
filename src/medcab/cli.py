from __future__ import annotations

from apps.cli import cli
from core.dependencies import APP_SETTINGS
from red_utils.ext.loguru_utils import LoguruSinkStdOut, init_logger

if __name__ == "__main__":
    init_logger([LoguruSinkStdOut(level=APP_SETTINGS.log_level).as_dict()])

    cli()
