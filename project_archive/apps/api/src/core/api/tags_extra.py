from __future__ import annotations

API_METHOD_TAGS: list[dict[str, str]] = [
    {"name": "GET", "description": "Endpoints requested with GET method."},
    {"name": "POST", "description": "Endpoints requested with POST method. Some kind of data is usually passed, either in the form or URL params or a request body."},
    {"name": "PUT", "description": "Endpoints requested with PUT method. Unlike PATCH requests, PUT request bodies must contain all possible parameters with values for each."},
    {"name": "DELETE", "description": "Endpoints requested with DELETE method."},
    {"name": "PATCH", "description": "Endpoints requested with PATCH method. Accepts a partial object, where only parameters with updated values are passed. Used to make partial updates to an existing object."}
]
ENDPOINT_GROUPS: list[dict[str, str]] = [{
    "name": "products",
    "description": "Endpoints for interacting with Products in MedCab.",
}, ]
