from pydantic import BaseModel, Field, validator, ValidationError
from typing import Union

from .base import PageNotificationBase


class PageNotificationGeneric(PageNotificationBase):
    """Simple, generic notification object."""

    success: bool | None = Field(default=None)
    data: dict | None = Field(default=None)
