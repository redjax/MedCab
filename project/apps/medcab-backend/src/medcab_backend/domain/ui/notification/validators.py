from flask import Request

from typing import Union
from .alerts import PageNotificationGeneric

from loguru import logger as log

def validate_notification(request: Request = None) -> Union[PageNotificationGeneric, None]:
    """Extract notification arg from incoming request & return as a parsed PageNotificationGeneric."""
    if request is None:
        return_obj = None
    if request.args.get("notification") is not None:
        try:
            return_obj: PageNotificationGeneric = PageNotificationGeneric.model_validate_json(request.args.get("notification"))
        except Exception as exc:
            log.error(Exception(f"Unhandled exception extracting notification from request object. Details: {exc}"))
            
            return None
    else:
        return_obj = None
        
    return return_obj