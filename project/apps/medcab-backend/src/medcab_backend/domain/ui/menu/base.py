from pydantic import BaseModel, Field, field_validator, ValidationError
from typing import Union
from pathlib import Path

from loguru import logger as log


class DropdownMenuOptionsBase(BaseModel):
    pass
