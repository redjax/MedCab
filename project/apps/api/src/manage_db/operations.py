import sys
sys.path.append(".")

from typing import Union
from pathlib import Path

import json
import httpx
import time

from .schemas import APIServer
from core.constants import DATA_DIR
from core.config import app_settings, api_settings

from pydantic import BaseModel, Field, field_validator, ValidationError
from loguru import logger as log

from red_utils.ext.loguru_utils import init_logger, LoguruSinkStdOut
from red_utils.ext.httpx_utils import default_headers, constants, get_req_client, merge_headers, update_headers
from red_utils.ext.fastapi_utils import default_openapi_url
from red_utils.std.path_utils import crawl_dir

import httpx


def test_connection(client: httpx.Client = None, url: str = None) -> bool:
    """Test connection by pinging an endpoint that will return a 200 response if online.
    
    Params:
    -------
    - client (httpx.Client): HTTPX request client.
    - url (str): The URL to request.
    """
    if client is None:
        raise ValueError("Missing an HTTPX client")
    if url is None:
        raise ValueError("Missing a request URL")

    try:
        with client as c:
            res = c.get(url)
            
            if res.status_code == 200:
                return True
            else:
                log.warning(f"Non-success response: [{res.status_code}: {res.reason_phrase}]")
                
                return False
            
    except Exception as exc:
        log.error(Exception(f"Unhandled exception running connectivity test. Details: {exc}"))
        
        return False


def load_json_files(files: list[Path]) -> list[dict]:
    """Load JSON files into a list of dict objects.
    
    Params:
    -------
    - files (list[Path]): A list of Path objects that are .json files.
    """
    if files is None:
        raise ValueError("List of file paths is empty or None")

    return_objs: list[dict] = []
    
    for f in files:
        if not f.is_file():
            pass
        log.info(f"Loading sample Product from: {f}")
        
        try:
            with open(f, "r") as read_file:
                lines = read_file.read()
                data = json.loads(lines)
            
            return_objs.append(data)

        except Exception as exc:
            msg = Exception(f"Unhandled exception loading JSON data from file: {f}. Details: {exc}")
            log.error(msg)
            
            pass
        
    log.debug(f"Loaded [{len(return_objs)}] dict object(s).")
    
    return return_objs


def insert_product_into_db(client: httpx.Client = None, product_dict: dict = None, url: str = None) -> bool:
    if client is None:
        raise ValueError("Missing HTTPX client")
    if product_dict is None:
        raise ValueError("Missing a Product dict")
    if url is None:
        raise ValueError("Missing URL to send POST request to")
    
    log.info(f"Uploading Product: {product_dict}")
    log.debug(f"POST URL: {url}")
    
    with client as c:
        try:
            req_data = json.dumps(product_dict)
            
            if not req_data:
                log.warning(f"JSON for product [{product_dict['strain']}] is empty. Skipping")
                
                return False
            
            insert_res = c.post(url, data=req_data)
            log.debug(f"[{insert_res.status_code}: {insert_res.reason_phrase}]")
            
            if insert_res.status_code == 200:
                log.info(f"Success: insert [{product_dict['strain']}]")
                
                return True
            
            elif insert_res.status_code in [400, 500]:
                log.error(f"[{insert_res.status_code}: {insert_res.reason_phrase}]: {insert_res.text}")
                return False
            else:
                log.warning(f"Non-200 response: [{insert_res.status_code}: {insert_res.reason_phrase}]")
                return False
            
        except ConnectionResetError as conn_reset:
            log.error(
                ConnectionResetError(f"Connection was reset. Details: {conn_reset}")
            )
            
            return False

        except Exception as exc:
            log.error(
                Exception(f"Unhandled exception posting data to API. Details: {exc}")
            )

            return False

def loop_insert_products(products: list[dict] = None, api: APIServer = None, pause_between: bool = False) -> dict[str, list[dict]]:
    """Loop over a list of dict objects and make requests to insert them into the database.
    
    Params:
    -------
    - products (list[dict]): List of Product dicts.
    - api (APIServer): An initialized APIServer instance
    """
    if products is None:
        raise ValueError("List of Product dicts is empty or None")
    if api is None:
        raise ValueError("Missing APIServer instance")
    
    successes: list[dict] = []
    failures: list[dict] = []
    
    for p in products:
        
        httpx_client: httpx.Client = get_req_client(headers=default_headers)
        
        try:
            insert_res = insert_product_into_db(client=httpx_client, product_dict=p, url=f"{api.base_url}{api.api_str}/products/create")
            
            if insert_res:
                log.info(f"Successfully inserted [{p['strain']}] into database")
                successes.append(p)
            if not insert_res:
                log.error(f"Error inserting [{p['strain']}] into database")
                failures.append(p)
        
        except Exception as exc:
            msg = Exception(f"Unhandled exception inserting Product [{p['strain']}]. Details: {exc}")
            log.error(msg)
            failures.append(p)
            
            pass
        
        if pause_between:
            input("PAUSE BEFORE NEXT INSERT...")
        
    log.debug(f"Successes: [{len(successes)}]. Failures: [{len(failures)}]")
    
    return {"successes": successes, "failures": failures}


def insert_samples(api: APIServer = None, products_json_dir: Path = None, pause_between_inserts: bool = False):
    """Load samples from data directory & insert them into database via HTTP request.
    
    Params:
    -------
    - api (APIServer): An initialized APIServer object.
    - products_json_dir (Path): Path where sample .JSON files are stored. These files will be loaded into
        objects that will be passed to the API to create them in the database.
    """
    if api is None:
        raise ValueError("Missing APIServer object")
    if products_json_dir is None:
        raise ValueError("Missing path to .json files")

    sample_dir_crawl: dict[str, list["str"]] = crawl_dir(in_dir=products_json_dir, ext_filter=".json")
    sample_files: list[Path] = sample_dir_crawl["files"]
    log.info(f"Found [{len(sample_files)}] simplified example Product(s)")
    
    if sample_files is not None and len(sample_files) > 0:
        for f in sample_files:
            log.debug(f"File: {f}")
    else:
        log.warning(f"No files found in directory: {products_json_dir}")
        return
        
    sample_dicts: list[dict] = load_json_files(sample_files)
    
    if sample_dicts:
        log.debug(f"Sample: {sample_dicts[0]}")

    connection_test_client: httpx.Client = get_req_client(headers=default_headers)
    conn_test_results = test_connection(client=connection_test_client, url=api.healthcheck_url)
    log.info(f"Connection test success: {conn_test_results}")
    
    if not conn_test_results:
        log.error(Exception(f"Connection test was not successful. Exiting app."))
        exit(1)
        
    insert_products = loop_insert_products(products=sample_dicts, api=api, pause_between=pause_between_inserts)
    log.debug(f"Insert products res: {type(insert_products)}. Keys: {insert_products.keys()}")
    
    if len(insert_products["successes"]) >0:
        for s in insert_products["successes"]:
            log.debug(f"Success ({type(s)}): {s}")
            
    if len(insert_products["failures"]) > 0:
        for f in insert_products["failures"]:
            log.debug(f"Failure ({type(f)}): {f}")
            
    return insert_products


def remove_all_items(api: APIServer = None) -> bool:
    remove_choice: str = input("Remove all Products from the database? [Y/N]: ")
    url: str = f"{api.base_url}/api/v1/products/all"

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
        remove_all_items(api=api)