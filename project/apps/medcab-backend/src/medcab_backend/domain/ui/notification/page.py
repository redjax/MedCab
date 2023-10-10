from pydantic import BaseModel, Field, validator, ValidationError
from typing import Union

from .base import PageDataBase
from .alerts import PageNotificationGeneric


class PageData(PageDataBase):
    notification: PageNotificationGeneric | None = Field(default=None)
