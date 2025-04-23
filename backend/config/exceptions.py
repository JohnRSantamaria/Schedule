from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import traceback
import logging

logger = logging.getLogger(__name__)

# Mapeo de clases a tipos legibles
EXCEPTION_TYPE_MAP = {
    "ValidationError": "validation_error",
    "AuthenticationFailed": "authentication_failed",
    "NotAuthenticated": "authentication_required",
    "PermissionDenied": "permission_denied",
    "NotFound": "not_found",
    "ParseError": "bad_request",
    "MethodNotAllowed": "method_not_allowed",
    "Throttled": "rate_limited",
}

def get_error_type(exc):
    return EXCEPTION_TYPE_MAP.get(exc.__class__.__name__, "internal_error")

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    exc_type = get_error_type(exc)

    error_payload = {
        "success": False,
        "type": exc_type,
    }

    if response is not None:
        logger.warning(f"DRF Exception: {exc_type}", exc_info=True)
        error_payload["error"] = response.data
        status_code = response.status_code
    else:
        logger.error(f"Unhandled Exception: {exc_type}", exc_info=True)
        error_payload["error"] = str(exc)
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    # Incluir trazas de error si estamos en DEBUG
    if settings.DEBUG:
        error_payload["trace"] = traceback.format_exc()

    return Response(error_payload, status=status_code)