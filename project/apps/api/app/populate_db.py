from typing import Union, Optional
from pathlib import Path

import json
import httpx
import time

from pydantic import BaseModel, Field, field_validator, ValidationError

from config import settings
from loguru import logger as log


from red_utils.httpx_utils import (
    default_headers,
    constants,
    get_req_client,
    make_request,
    merge_headers,
    update_headers,
)

example_schemas: Path = Path("example_schemas")
example_products: Path = Path(f"{str(example_schemas)}/products/simplified_for_testing")


class APIServer(BaseModel):
    proto: str = Field(default="http")
    url: str = Field(default="127.0.0.1")
    port: int = Field(default=8000)
    api_str: str = Field(default=f"/api/v1")

    @property
    def base_url(self) -> str:
        _url: str = f"{self.proto}://{self.url}:{self.port}"

        return _url

    @property
    def base_api_url(self) -> str:
        _url: str = f"{self.base_url}{self.api_str}"

        return _url

    @property
    def healthcheck_url(self) -> str:
        _url: str = f"{self.base_url}/health"

        return _url

    @field_validator("proto")
    def validate_prototype(cls, v) -> str:
        valid_protos: list[str] = ["http", "https"]

        if not v in valid_protos:
            raise ValueError(f"Invalid proto: {v}. Must be one of {valid_protos}")

        return v


# api: APIServer = APIServer(url="192.168.1.30", port=8001)
api: APIServer = APIServer(port=8001)
log.debug(f"API URL string: {api.base_url}")

client = get_req_client(headers=default_headers)
connectivity_test_client: httpx.Client = get_req_client(headers=default_headers)


def test_connection(
    client: httpx.Client = None, url: str = f"{api.healthcheck_url}"
) -> bool:
    try:
        with client as c:
            res = c.get(url)

            if res.status_code == 200:
                return True
            else:
                log.warning(
                    f"Non-success response: [{res.status_code}: {res.reason_phrase}]"
                )

                return False
    except Exception as exc:
        log.error(
            Exception(f"Unhandled exception running connectivity test. Details: {exc}")
        )
        return False


def load_json_data_objs(
    search_path: Union[str, Path] = None, search_suffix: str = ".json"
) -> list[dict]:
    if not search_path:
        raise ValueError("Missing path to scan")
    if not isinstance(search_path, Path):
        if isinstance(search_path, str):
            search_path: Path = Path(search_path)
        else:
            raise TypeError(
                f"Invalid type for search_path: ({type(search_path)}). Must be one of [str, pathlib.Path]"
            )

    files: list[Path] = []
    for _f in search_path.iterdir():
        files.append(_f)

    if files:
        log.debug(
            f"Cleaning list, searching for ({search_suffix}) files. Starting count: [{len(files)}]"
        )
        new_files: list[Path] = []
        for _f in files:
            if _f.suffix == ".json":
                new_files.append(_f)

        log.debug(
            f"Cleaned [{len(files) - len(new_files)}] file(s) from starting list."
        )
        files = new_files
    else:
        log.warning(f"No files found at {example_products}")
        return None

    return_objs: list[dict] = []

    for f in files:
        try:
            with open(f, "r+") as f:
                data = f.read()
                _json = json.loads(data)

                product: dict = _json

                return_objs.append(product)

        except Exception as exc:
            raise Exception(
                f"Unhandled exception loading data from file: {str(f)}. Details: {exc}"
            )

    return return_objs


def load_data_into_db(
    data: list[dict] = [],
    client: httpx.Client = None,
    url: str = f"{api.base_api_url}/products/create",
) -> dict[str, Union[bool, list[httpx.Response], list[dict], str, Exception, None]]:
    log.debug(f"POST URL: {url}")

    success_responses: list[httpx.Response] = []
    non_success_responses: list[httpx.Response] = []

    return_obj: dict = {
        "success": None,
        "responses": [
            {"success": success_responses},
            {"failure": non_success_responses},
        ],
        "detail": None,
    }

    with client as c:
        try:
            for product in data:
                # log.debug(f"Product dict ({type(product)}): {product}")
                _json = json.dumps(product)
                # log.debug(f"Product JSON ({type(_json)}): {_json}")

                if not _json:
                    log.warning(
                        f"JSON for product [{product['strain']}] is empty. Skipping"
                    )
                    pass

                log.debug(
                    f"Making POST request to create product '{product['strain']}'"
                )

                res = c.post(url, data=_json)
                log.debug(
                    f"Load data response: [{res.status_code}: {res.reason_phrase}]"
                )

                if res.status_code == 200:
                    log.debug(f"Product [{product['strain']}] created successfully.")
                    success_responses.append(res)
                elif res.status_code == 409:
                    log.debug(
                        f"Product [{product['strain']}] already exists in database."
                    )
                    success_responses.append(res)
                elif res.status_code == 400:
                    log.debug(f"URL not found: {res.url}")
                    non_success_responses.append(res)
                elif res.status_code == 500:
                    log.error(
                        f"Fatal server error on strain: [{product['strain']}]. Response: [{res.status_code}: {res.reason_phrase}]: {res.text}"
                    )
                    non_success_responses.append(res)
                    time.sleep(0.01)
                    pass
                else:
                    log.warning(
                        f"Non-success response: [{res.status_code}: {res.reason_phrase}]: {res.text}"
                    )
                    non_success_responses.append(res)
                    time.sleep(0.01)
                    pass

                time.sleep(0.01)

        except ConnectionResetError as conn_reset:
            log.error(
                ConnectionResetError(f"Connection was reset. Details: {conn_reset}")
            )
            time.sleep(0.01)
            pass
        except Exception as exc:
            log.error(
                Exception(f"Unhandled exception posting data to API. Details: {exc}")
            )

            return_obj: dict[
                str, Union[bool, Exception, list[dict[str, list[httpx.Response]]]]
            ] = {
                "success": False,
                "responses": [
                    {"success": success_responses},
                    {"failure": non_success_responses},
                ],
                "detail": exc,
            }
            return return_obj

    return_obj: dict[
        str, Union[bool, Exception, list[dict[str, list[httpx.Response]]]]
    ] = {
        "success": True,
        "responses": [
            {"success": success_responses},
            {"failure": non_success_responses},
        ],
        "detail": None,
    }

    return return_obj


def remove_all_items() -> bool:
    remove_choice: str = input("Remove all Products from the database? [Y/N]: ")
    url: str = f"{api.base_api_url}/products/all"

    delete_client: httpx.Client = get_req_client(headers=default_headers)

    if remove_choice in ["Y", "y"]:
        _confirm = input(
            "Confirm you want to delete all Products from the database [Y/N]: "
        )

        if _confirm in ["Y", "y"]:
            try:
                with delete_client as c:
                    res = c.delete(url)
                    log.debug(
                        f"Delete all Products response: [{res.status_code}: {res.reason_phrase}]: {res.text}"
                    )

                    if res.status_code in [200, 202]:
                        log.info("Successfully deleted all Products.")
                        return True
                    elif res.status_code == 404:
                        log.warning("No Products exist in database")
                        return True
                    else:
                        log.error(f"Error deleting all Products.")
                        return False
            except Exception as exc:
                log.error(
                    Exception(
                        f"Unhandled exception deleting all Products. Details: {exc}"
                    )
                )
                return False
        elif _confirm in ["N", "n"]:
            log.info(f"Skipping deleteion")

            return False
    elif remove_choice in ["N", "n"]:
        log.info("Skipping deletion")
        return False
    else:
        log.error(f"Invalid choice: {remove_choice}")
        remove_all_items()


log.info(f"Loading products from {example_products}")
products = load_json_data_objs(search_path=example_products)
log.info(f"Loaded [{len(products)}] products into dicts")
log.debug(f"Products: {products}")

log.info(f"Testing connection to {api.healthcheck_url}")
connectivity: bool = test_connection(client=connectivity_test_client)
log.info(f"Connection success: [{connectivity}]")

log.info(f"Populating database with [{len(products)}] products")
load_success = load_data_into_db(client=client, data=products)
log.debug(f"Load success ({type(load_success)}): {load_success}")

_remove = remove_all_items()
