from pathlib import Path
import os

from flask import (
    Blueprint,
    abort,
    request,
    Response,
    jsonify,
    redirect,
    url_for,
    flash,
    current_app,
    render_template,
)

from .form_schemas import NewProductform

import attrs
from loguru import logger as log

from medcab_backend.domain.product import Product
from medcab_backend.constants import ENV
from medcab_backend.domain.product.validators import valid_families, valid_forms

products_app = Blueprint("products", __name__)


@products_app.route("/", methods=["GET"])
def index() -> dict[str, str]:
    if request.method == "GET":
        # return jsonify({"msg": "Products root reached"})
        return render_template(
            "pages/products/index.html", app_env=ENV, page_name="products"
        )


@products_app.route("/new", methods=["GET"])
def new_product_page():
    return render_template(
        "pages/products/new/index.html",
        app_env=ENV,
        page_name="new_product",
        valid_forms=valid_forms,
        valid_families=valid_families,
    )


@products_app.route("/new", methods=["post"])
def create_new_product():
    ## Check header type, handle application/json and multipart/form-data
    content_type = request.headers.get("Content-Type")
    log.info(f"Received POST request, content-type: {content_type}")

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

            return redirect(url_for("products.new_product_page"))

        log.debug(f"Incoming product data: {new_product_form.data}")
        if new_product_form.errors:
            log.error(f"Form validation errors: {new_product_form.errors}")

        try:
            if new_product_form.validate():
                new_product = Product(**new_product_form.data)

                log.debug(f"New product: {new_product}")
            else:
                log.error(
                    f"Unable to validate new product form input. Details: {new_product_form.errors}"
                )

            return redirect(url_for("products.new_product_page"))

        except Exception as exc:
            log.error(
                Exception(
                    f"Unhandled exception validating form & converting to Product object. Details: {exc}"
                )
            )

            return redirect(url_for("products.new_product_page"))

    ## Non JSON/web form data
    else:
        return redirect(url_for("product.new_product_page"))
