from __future__ import annotations

from pathlib import Path
from typing import Union

from loguru import logger as log
from pydantic import BaseModel, Field, ValidationError, field_validator

class DropdownMenuOptionsBase(BaseModel):
    pass
