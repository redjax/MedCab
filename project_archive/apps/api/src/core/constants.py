from __future__ import annotations

from pathlib import Path

from core.api.tags_extra import API_METHOD_TAGS, ENDPOINT_GROUPS
from core.enums import FamilyEnum, FormEnum

DATA_DIR: Path = Path(".data")
CACHE_DIR: Path = Path(".cache")
SERIALIZE_DIR: Path = Path(".serialize")

## Join all custom tag lists into one list
CUSTOM_TAGS: list[dict[str,str]] = API_METHOD_TAGS + ENDPOINT_GROUPS
