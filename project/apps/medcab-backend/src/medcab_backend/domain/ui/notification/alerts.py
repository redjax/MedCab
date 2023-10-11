from __future__ import annotations

from typing import Any, Union

from .base import PageNotificationBase

from pydantic import BaseModel, Field, ValidationError, validator

class PageNotificationGeneric(PageNotificationBase):
    """Simple, generic notification object."""

    success: bool | None = Field(default=None)
    data: dict | None = Field(default=None)

    def format_for_send(self) -> str:
        """Return this model in JSON string format for sending across endpoints."""
        _json = self.model_dump_json()

        return _json
