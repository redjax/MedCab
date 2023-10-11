from __future__ import annotations

from pathlib import Path
from typing import Any, Union

from .base import DropdownMenuOptionsBase

from loguru import logger as log
from pydantic import BaseModel, Field, ValidationError, field_validator

class DropdownMenuOptions(DropdownMenuOptionsBase):
    options: list[Union[str, int, Any]] = Field(default=None)
