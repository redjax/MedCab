from __future__ import annotations

from typing import Union

from loguru import logger as log

# from settings.config import app_settings, logging_settings
from config import settings

# from red_utils.fastapi_utils import default_api_str, tags_metadata

# ENV: str = app_settings.APP_ENV
ENV: str = settings.fastapi["env"]
