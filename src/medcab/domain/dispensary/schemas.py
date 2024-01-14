from __future__ import annotations

from datetime import date, datetime, time
from decimal import Decimal
from pathlib import Path
from typing import Any, Optional, Union
import uuid

from core.validators.product import VALID_FAMILIES, VALID_FORMS
from loguru import logger as log
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationError,
    computed_field,
    field_validator,
)

class DispensaryBase(BaseModel):
    favorite: bool = Field(default=False)
    name: str = Field(default=None)
    city: str = Field(default=None)
    state: str = Field(default=None)


class DispensaryCreate(DispensaryBase):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID

    # class Config:
    #     from_attributes = True


class DispensaryUpdate(DispensaryBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID | None = None
    name: str | None = None
    city: str | None = None
    state: str | None = None


class Dispensary(DispensaryBase):
    pass
