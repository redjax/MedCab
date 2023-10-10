from pydantic import BaseModel, validator, ValidationError, Field
from typing import Union
from decimal import Decimal


class PageNotificationBase(BaseModel):
    """Store content for a notification or alert."""

    message: str | None = Field(default=None)
    display: bool = Field(default=False)


class PageDataBase(BaseModel):
    """Base PageData object.

    Do not use this class directly, use PageData.
    """

    page_name: str | None = Field(Default=None)
