from pydantic import BaseModel, Field, field_validator, ValidationError
from typing import Union, Any
from pathlib import Path

from loguru import logger as log

from .base import DropdownMenuOptionsBase


class DropdownMenuOptions(DropdownMenuOptionsBase):
    options: list[Union[str, int, Any]] = Field(default=None)
