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
)

import attrs
from loguru import logger as log

products_app = Blueprint("products", __name__)


@products_app.route("/", methods=["GET"])
def index() -> dict[str, str]:
    if request.method == "GET":
        return jsonify({"msg": "Products root reached"})
