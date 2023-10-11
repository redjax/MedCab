from __future__ import annotations

from typing import Union

from .alerts import PageNotificationGeneric
from .base import PageDataBase

from pydantic import BaseModel, Field, ValidationError, validator

class PageData(PageDataBase):
    notification: PageNotificationGeneric | None = Field(default=None)
