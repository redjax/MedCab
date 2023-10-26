from __future__ import annotations

from decimal import Decimal
from typing import Union

from pydantic import BaseModel, Field, ValidationError, validator

class PageNotificationBase(BaseModel):
    """Store content for a notification or alert."""

    message: str | None = Field(default=None)
    display: bool = Field(default=False)


class PageDataBase(BaseModel):
    """Base PageData object.

    Do not use this class directly, use PageData.
    """

    page_name: str | None = Field(Default=None)
