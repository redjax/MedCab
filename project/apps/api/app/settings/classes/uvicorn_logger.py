from __future__ import annotations

import logging

from logging.config import dictConfig
from typing import Optional, Union

from pydantic import BaseModel, Field, ValidationError, validator
from pydantic_settings import BaseSettings

default_uvicorn_fmt: str = (
    '%(levelprefix)s %(asctime)s - %(client_addr)s - "%(request_line)s" %(status_code)s'
)
default_uvicorn_datefmt: str = "%Y-%m-%d_%H:%M:%S"


def get_uvicorn_config(
    uvicorn_level: str = "DEBUG",
    uvicorn_err_level: str = "ERROR",
    uvicorn_logger_ver: int = 1,
    name: str = "__main__",
) -> dict:
    """Generate a Uvicorn logging config with defaults and return as dict."""
    ## Config dict to be passed into Uvicorn logger class
    uvicorn_log_config = {
        "version": uvicorn_logger_ver,
        "disable_existing_loggers": False,
        "formatters": {
            "access": {
                "()": "uvicorn.logging.AccessFormatter",
                "fmt": default_uvicorn_fmt,
                "datefmt": default_uvicorn_datefmt,
                "use_colors": True,
            },
            "default": {
                "()": "uvicorn.logging.DefaultFormatter",
                "fmt": "%(levelprefix)s %(asctime)s - %(message)s",
                # "datefmt": "%Y-%m-%d %H:%M:%S",
                "datefmt": default_uvicorn_datefmt,
                "use_colors": True,
            },
        },
        "handlers": {
            "access": {
                "class": "logging.StreamHandler",
                "formatter": "access",
                "stream": "ext://sys.stdout",
            },
            "default": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stderr",
            },
        },
        "loggers": {
            name: {"handlers": ["default"], "level": "DEBUG", "propagate": False},
            "uvicorn": {"handlers": ["default"], "level": "DEBUG", "propagate": True},
            "uvicorn.access": {
                "handlers": ["access"],
                # "level": "INFO",
                "level": uvicorn_level,
                "propagate": False,
            },
            "uvicorn.error": {
                # "level": "INFO",
                "level": uvicorn_err_level,
                "propagate": False,
            },
        },
    }

    return uvicorn_log_config


class CustomUvicornLogConfig(BaseModel):
    # name: str = "main"
    # version: int = 1
    # disable_existing_loggers: bool = False
    # use_colors: bool = True
    # level: str = "INFO"

    # @validator("level")
    # def validate_level(self) -> str:
    #     print(self.level)
    #     if not self.level.isupper():
    #         self.level: str = self.level.upper()

    #     return self.level

    # log_config: dict = {}

    log_config: dict = Field(default_factory=get_uvicorn_config)


default_uvicorn_logging: CustomUvicornLogConfig = CustomUvicornLogConfig()


# def append_uvicorn_logger(
#     base_logger: logging.Logger = None,
#     uvicorn_config: CustomUvicornLogger = CustomUvicornLogger(),
# ):
#     log_config = get_uvicorn_config()
#     logging.config.dictConfig(log_config)

#     base_logger = logging.getLogger(name)

#     return base_logger
