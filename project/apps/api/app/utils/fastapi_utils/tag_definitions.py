"""Define custom FastAPI endpoint tags.

The tags_metadata object can be imported by the main FastAPI app.
As endpoints are created, their metadata can be defined here as
a list object.
"""
from __future__ import annotations

from typing import Union


def compile_tag_metadata(
    tags_metadata: list[dict[str, str]] = None,
    new_data: list[dict[str, str]] = None,
    allow_empty: bool = True,
) -> list[dict[str, str]]:
    """Compile new tag metadata objects into tags_metadata list.

    Accepts a list of dicts, formatted as {"name": ..., "description": ...}. These objects describe metadata
    for the OpenAPI docs site.

    This function is meant to run once at app startup.

    The 'allow_empty' parameter allows for new_data to be an empty list or None. This is to handle new apps that
    have not created any custom tag metadata objects at startup.

    allow_empty only applies to new_data. An initial tags_metadata object must be submitted.
    """
    if not tags_metadata:
        raise ValueError("Missing tags_metadata object.")

    if not isinstance(tags_metadata, list):
        raise TypeError(
            f"Invalid type for tags_metadata: ({type(tags_metadata)}). Must be of type list[dict]"
        )

    for _ in tags_metadata:
        if not isinstance(_, dict):
            raise TypeError(
                f"Invalid type for metadata dict '{_['name']}: ({type(_)}). Must be of type dict."
            )

    if not new_data:
        if not allow_empty:
            raise ValueError("Missing input dict to append to tags_metadata")

    if not isinstance(new_data, list):
        raise TypeError(
            f"Invalid type for new_data: ({type(new_data)}). Must be of type list."
        )

    for _ in new_data:
        if not isinstance(_, dict):
            raise TypeError(
                f"Invalid type for metadata dict '{_['name']}: ({type(_)}). Must be of type dict."
            )

    new_metadata = tags_metadata.copy()

    for _tag in new_data:
        if not _tag in new_metadata:
            new_metadata.append(_tag)

    return new_metadata


## Add metadata to tags assigned throughout the app. If a router/endpoint's tags match
#  any of these, the description and other metadata will be applied on the docs page.
#  This tags_metadata can be imported and extended with tags_metadata.append(new_tags_dict).
#
#  You can also create a new list of tags ([{"name": ..., "description": ...}, ...]) and join
#  them with tags_metadata = tags_metadata + new_tags_list
default_tags_metadata = [
    {
        "name": "default",
        "description": "Tags have not been added to these endpoints/routers.",
    },
    {
        "name": "util",
        "description": "Utility functions, routes, & more. These utils are in the root of the app, and accessible by all sub-apps and routers.",
    },
]


products_metadata = {
    "name": "products",
    "description": "Brands, items, forms, & more info about purchased products.",
}

## Add metadata dicts to this list to have them compiled into the main tags_metadata object.
append_metadata = [products_metadata]

tags_metadata = compile_tag_metadata(
    tags_metadata=default_tags_metadata, new_data=append_metadata
)
