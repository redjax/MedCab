from pydantic import BaseModel, Field, validator, ValidationError
from typing import Union, Any

from .base import PageNotificationBase


class PageNotificationGeneric(PageNotificationBase):
    """Simple, generic notification object."""

    success: bool | None = Field(default=None)
    data: dict | None = Field(default=None)
    
    def format_for_send(self) -> str:
        """Return this model in JSON string format for sending across endpoints."""
        _json = self.model_dump_json()
        
        return _json
