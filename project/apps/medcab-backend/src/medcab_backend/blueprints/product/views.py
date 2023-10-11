from __future__ import annotations

import json
import os

from pathlib import Path
from typing import Union

from medcab_backend.constants import ENV
from medcab_backend.dependencies import dropdown_family, dropdown_form
from medcab_backend.domain.product import (
    Product,
    ProductResponse,
    crud as product_crud,
)
from medcab_backend.domain.product.form_schemas import NewProductform
from medcab_backend.domain.product.models import ProductModel
from medcab_backend.domain.ui.notification import (
    PageNotificationGeneric,
    validate_notification,
)

import attrs

from flask import (
    Blueprint,
    Request,
    Response,
    abort,
    current_app,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
from loguru import logger as log

products_app = Blueprint("products", __name__)


def validate_notification(
    request: Request = None,
) -> Union[PageNotificationGeneric, None]:
    """Extract notification arg from incoming request & return as a parsed PageNotificationGeneric."""
    if request is None:
        return_obj = None
    if request.args.get("notification") is not None:
        try:
            return_obj: PageNotificationGeneric = (
                PageNotificationGeneric.model_validate_json(
                    request.args.get("notification")
                )
            )
        except Exception as exc:
            log.error(
                Exception(
                    f"Unhandled exception extracting notification from request object. Details: {exc}"
                )
            )

            return None
    else:
        return_obj = None

    return return_obj


@products_app.route("/", methods=["GET"])
def index() -> dict[str, str]:
    if request.args.get("notification"):
        notification = validate_notification(request=request)
    else:
        notification = None

    try:
        db_products: list[ProductModel] = product_crud.get_all_products()
        log.debug(f"Loaded [{len(db_products)}] from database.")

        all_products: list[ProductResponse] = []

        for p in db_products:
            product_response: ProductResponse = ProductResponse(
                id=p.id,
                favorite=p.favorite,
                strain=p.strain,
                family=p.family,
                form=p.form,
                total_cbd=p.total_cbd,
                total_thc=p.total_thc,
            )

            all_products.append(product_response)

    except Exception as exc:
        log.error(
            Exception(
                f"Unhandled exception getting all Products from DB. Details: {exc}"
            )
        )
        all_products = None

    if request.method == "GET":
        return render_template(
            "pages/products/index.html",
            app_env=ENV,
            page_name="products",
            products_list=all_products,
            valid_forms=dropdown_form.options,
            valid_families=dropdown_family.options,
            notification=notification,
        )


@products_app.route("/new", methods=["GET"])
def new_product_page():
    notification = validate_notification(request)

    return render_template(
        "pages/products/new/index.html",
        app_env=ENV,
        page_name="new_product",
        valid_forms=dropdown_form.options,
        valid_families=dropdown_family.options,
        notification=notification,
    )


@products_app.route("/new", methods=["post"])
def create_new_product():
    ## Check header type, handle application/json and multipart/form-data
    content_type = request.headers.get("Content-Type")
    log.info(f"Received POST request, content-type: {content_type}")

    notification = validate_notification(request)

    ## Parse incoming JSON data, i.e. from an API call
    if content_type == "application/json":
        log.debug(f"Detected JSON data")

        try:
            ## Convert to Product object
            product: Product = Product(**request.json)
            log.debug(f"Product: {product}")

            return Response(
                product.model_dump_json(), status=201, mimetype="application/json"
            )
        except TypeError as type_err:
            log.error(
                TypeError(
                    f"TypeError converting incoming request to Product object. Details: {type_err}"
                )
            )

            ## Return 400 malformed request
            return Response(
                f"Unable to convert request to Product object. Request object may be misformed. Details: {type_err}",
                status=400,
                mimetype="application/json",
            )
        except Exception as exc:
            log.error(
                f"Unhandled exception converting request to Product object. Details: {exc}"
            )

            ## Return 500 internal/unhandled server error
            return Response(
                {"error": "Internal Server Error"},
                status=500,
                mimetype="application/json",
            )

    ## Web form data
    elif "multipart/form-data" in content_type:
        log.debug(f"Web form data received. Attempting to parse as form")

        try:
            new_product_form = NewProductform(request.form)

        except Exception as exc:
            log.error(
                Exception(
                    f"Unhandled exception parsing input data. Content-Type: {content_type}. Details: {exc}"
                )
            )

            notification = PageNotificationGeneric(
                message="Unable to parse form input.",
                display=True,
                success=False,
                data={"exception": exc},
            )
            return redirect(
                url_for("products.index", notification=notification.model_dump_json())
            )

        log.debug(f"Incoming product data: {new_product_form.data}")
        if new_product_form.errors:
            log.error(f"Form validation errors: {new_product_form.errors}")

        if new_product_form.validate():
            try:
                log.debug(
                    f"Form data ({type(new_product_form.data)}): {new_product_form.data}"
                )
                new_product = Product.model_validate(new_product_form.data)
                log.debug(f"New product ({type(new_product)}): {new_product}")

                notification = PageNotificationGeneric(
                    message=f"Success: Added {new_product.strain}.",
                    display=True,
                    success=True,
                )

                ## Create product in database
                db_product = product_crud.create_product(product=new_product)
                log.debug(f"DB Product: {db_product}")

                return redirect(
                    url_for(
                        "products.new_product_page",
                        notification=notification.model_dump_json(),
                    )
                )

            except Exception as exc:
                log.error(
                    Exception(
                        f"Unhandled exception creating new Product object from form input. Details: {exc}"
                    )
                )

                notification = PageNotificationGeneric(
                    message=f"Error: Did not add new product, check server logs for details",
                    display=True,
                    success=False,
                )

                return redirect(
                    url_for(
                        "products.new_product_page",
                        notification=notification.model_dump_json(),
                    )
                )
        else:
            log.error(
                f"Unable to validate new product form input. Details: {new_product_form.errors}"
            )

            notification = PageNotificationGeneric(
                message="Unable to parse form input into Product object.",
                display=True,
                success=False,
                data={"details": new_product_form.errors},
            )

            return redirect(
                url_for(
                    "products.index",
                    valid_families=dropdown_form.options,
                    valid_forms=dropdown_family.options,
                    notification=notification.model_dump_json(),
                )
            )

    ## Non JSON/web form data
    else:
        return redirect(
            url_for("products.index"),
            valid_families=dropdown_form.options,
            valid_forms=dropdown_family.options,
            notification=PageNotificationGeneric(
                message=f"Received unsupported Content-Type: {content_type}",
                display=True,
                success=False,
            ).model_dump_json(),
        )
