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

import attrs
from loguru import logger as log

from medcab_backend.domain.product import Product

products_app = Blueprint("products", __name__)


@products_app.route("/", methods=["GET"])
def index() -> dict[str, str]:
    if request.method == "GET":
        # return jsonify({"msg": "Products root reached"})
        return render_template("pages/products/index.html")


@products_app.route("/new", methods=["GET"])
def new_product_page():
    # return render_template("pages/products/index.html")
    return {"message": "New product page not yet implemented"}


@products_app.route("/new", methods=["POST"])
def create_new_product():
    log.debug(f"Converting incoming request to Product object: {request.json}")

    try:
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

        return Response(
            f"Unable to convert request to Product object. Request object may be misformed. Details: {type_err}",
            status=400,
            mimetype="application/json",
        )
    except Exception as exc:
        log.error(
            f"Unhandled exception converting request to Product object. Details: {exc}"
        )

        return Response(
            {"error": "Internal Server Error"},
            status=500,
            mimetype="application/json",
        )
