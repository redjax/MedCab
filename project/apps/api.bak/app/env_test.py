from red_utils.loguru_utils import (
    default_app_log_file_sink,
    default_error_log_file_sink,
    default_stderr_color_sink,
    default_stderr_sink,
    default_stdout_color_sink,
    default_stdout_sink,
    default_trace_log_file_sink,
)

from red_utils.loguru_utils import init_logger
from red_utils.fastapi_utils import setup_uvicorn_logging
from loguru import logger as log

init_logger()


def debug_settings(sink_name: str = None, settings_dict: dict = None):
    if not sink_name:
        raise ValueError("Missing sink name")

    log.debug(f"Debugging [{sink_name}] sink:\n")

    for k, v in settings_dict.items():
        log.debug(f"Key: [{k}]. Value ({type(v)}): {v}")

    print("")


if __name__ == "__main__":
    ## app.log sink
    app_log_file: dict = {
        "sink_name": "app log",
        "settings_dict": default_app_log_file_sink,
    }

    # ## app.stderr sink
    stderr_color: dict = {
        "sink_name": "stderr",
        "settings_dict": default_stderr_color_sink,
    }

    # ## app.error sink
    error_log_file: dict = {
        "sink_name": "error log",
        "settings_dict": default_error_log_file_sink,
    }

    ## app.trace sink
    trace_log_file: dict = {
        "sink_name": "trace log",
        "settings_dict": default_trace_log_file_sink,
    }

    debug_settings(**trace_log_file)
