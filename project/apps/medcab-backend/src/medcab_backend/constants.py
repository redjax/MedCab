from __future__ import annotations

from dynaconf import settings

ENV: str = settings.ENV
CONTAINER_ENV: str = settings.CONTAINER_ENV

APP_NAME: str = settings.APP_NAME
APP_DESCRIPTION: str = settings.APP_DESCRIPTION
APP_VERSION: str = settings.APP_VERSION

APP_HOST: str = settings.APP_HOST
APP_PORT: int = settings.APP_PORT
APP_DEBUG: bool = settings.APP_DEBUG

## Openweathermap API key.
#  Retrieve from https://openweathermap.org
# OWM_API_KEY: str = settings.API_KEY
# BASE_URL: str = settings.BASE_URL

owm_conf: dict = settings.OWM_SETTINGS
