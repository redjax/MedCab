from __future__ import annotations

import ast

from medcab_backend.blueprints.product.views import products_app
from medcab_backend.constants import (
    APP_DESCRIPTION,
    APP_NAME,
    APP_VERSION,
    CONTAINER_ENV,
    ENV,
)
from medcab_backend.dependencies import dropdown_family, dropdown_form, engine
from medcab_backend.domain.ui import PageNotificationGeneric
from medcab_backend.domain.ui.notification import validate_notification

from dynaconf import settings
from flask import Flask, render_template, request
from loguru import logger as log
from red_utils.ext.loguru_utils import init_logger, sinks
from red_utils.ext.sqlalchemy_utils import Base, create_base_metadata

app = Flask(__name__)
app.secret_key = settings.APP_SECRET_KEY
app.register_blueprint(products_app, url_prefix="/products")


create_base_metadata(base_obj=Base, engine=engine)


@app.route("/", methods=["GET"])
def index() -> dict[str, str]:
    if request.args.get("notification"):
        notification = validate_notification(request=request)
    else:
        notification = None

    log.debug(f"MedCab Backend root page reached")
    # return {"msg": f"{APP_NAME} v{APP_VERSION} reached"}
    return render_template(
        "pages/index.html",
        app_env=ENV,
        page_name="home",
        valid_forms=dropdown_form.options,
        valid_families=dropdown_family.options,
        notification=notification,
    )


if __name__ == "__main__":
    log.debug(f"Settings: {settings.as_dict()}")
