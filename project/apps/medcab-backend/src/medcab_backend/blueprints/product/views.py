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
from medcab_backend.domain.ui import PageNotificationGeneric
from medcab_backend.constants import ENV
from medcab_backend.domain.product.validators import valid_families, valid_forms

import ast

products_app = Blueprint("products", __name__)


@products_app.route("/", methods=["GET"])
def index(notification: PageNotificationGeneric = None) -> dict[str, str]:
    if request.method == "GET":
        # notification_dict = request.args.get("notification")

        # if notification_dict is not None:
        #     notification = PageNotificationGeneric(
        #         **ast.literal_eval(notification_dict)
        #     )
        # else:
        #     notification = None

        return render_template(
            "pages/products/index.html",
            app_env=ENV,
            page_name="products",
            valid_forms=valid_forms,
            valid_families=valid_families,
            notification=notification,
        )


@products_app.route("/new", methods=["GET"])
def new_product_page(notification: PageNotificationGeneric = None):
    # notification_dict = request.args.get("notification")

    # if notification_dict is not None:
    #     notification = PageNotificationGeneric(**ast.literal_eval(notification_dict))
    # else:
    #     notification = None

    return render_template(
        "pages/products/new/index.html",
        app_env=ENV,
        page_name="new_product",
        valid_forms=valid_forms,
        valid_families=valid_families,
        notification=notification,
    )


@products_app.route("/new", methods=["post"])
def create_new_product(notification: PageNotificationGeneric = None):
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
        # notification_dict = request.args.get("notification")

        # log.debug(f"Notification dict ({type(notification_dict)}): {notification_dict}")

        # if notification_dict is not None:
        #     notification = PageNotificationGeneric(
        #         **ast.literal_eval(notification_dict)
        #     )
        # else:
        #     notification = None

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
            return redirect(url_for("products.index", notification=notification))

        log.debug(f"Incoming product data: {new_product_form.data}")
        if new_product_form.errors:
            log.error(f"Form validation errors: {new_product_form.errors}")

        try:
            if new_product_form.validate():
                new_product = Product(**new_product_form.data)

                log.debug(f"New product: {new_product}")

                notification = PageNotificationGeneric(
                    f"Success: Added {new_product.strain}.", display=True, success=True
                )

                return redirect(
                    url_for("products.new_product_page", notification=notification)
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
                    valid_families=valid_families,
                    valid_forms=valid_forms,
                    notification=notification,
                )
            )

        except Exception as exc:
            log.error(
                Exception(
                    f"Unhandled exception validating form & converting to Product object. Details: {exc}"
                )
            )

            notification = PageNotificationGeneric(
                message="Form validation failed.",
                display=True,
                success=False,
                data={"exception": exc},
            )

            return redirect(
                url_for("products.new_product_page", notification=notification)
            )

    ## Non JSON/web form data
    else:
        return Response(
            jsonify(
                {
                    "response": NotImplementedError(
                        f"Support for requests with Content-Type {content_type} not supported."
                    )
                },
                status=501,
            )
        )
