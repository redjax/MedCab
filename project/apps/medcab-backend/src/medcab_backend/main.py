from dynaconf import settings

from loguru import logger as log
from red_utils.ext.loguru_utils import init_logger, sinks

from flask import Flask, render_template, request
import ast

from medcab_backend.constants import (
    ENV,
    CONTAINER_ENV,
    APP_NAME,
    APP_VERSION,
    APP_DESCRIPTION,
)

from medcab_backend.blueprints.product.views import (
    products_app,
    valid_families,
    valid_forms,
)

from medcab_backend.domain.ui import PageNotificationGeneric

app = Flask(__name__)
app.secret_key = settings.APP_SECRET_KEY
app.register_blueprint(products_app, url_prefix="/products")


@app.route("/", methods=["GET"])
def index(notification: PageNotificationGeneric = None) -> dict[str, str]:
    # notification_dict = request.args.get("notification")

    # if notification_dict is not None:
    #     notification = PageNotificationGeneric(**ast.literal_eval(notification_dict))
    # else:
    #     notification = None

    log.debug(f"MedCab Backend root page reached")
    # return {"msg": f"{APP_NAME} v{APP_VERSION} reached"}
    return render_template(
        "pages/index.html",
        app_env="dev",
        page_name="home",
        valid_forms=valid_forms,
        valid_families=valid_families,
        notification=notification,
    )


if __name__ == "__main__":
    log.debug(f"Settings: {settings.as_dict()}")
