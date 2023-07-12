from __future__ import annotations


default_allow_credentials: bool = True
default_allowed_origins: list[str] = ["*"]
default_allowed_methods: list[str] = ["*"]
default_allowed_headers: list[str] = ["*"]


## Route to openapi docs. This returns the docs site as a JSON object
#  If you set this to the same route as docs (i.e. /docs), you will only
#  get the openapi JSON response, no Swagger docs.
default_openapi_url = "/docs/openapi"

default_api_str = "/api/v1"
