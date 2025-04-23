import logging
import traceback
from django.http import JsonResponse
from django.conf import settings

logger = logging.getLogger(__name__)

class GlobalExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            return self.get_response(request)
        except Exception as e:
            logger.error("Unhandled Exception in Middleware", exc_info=True)

            payload = {
                "success": False,
                "type": "internal_error",
                "error": str(e),
            }

            if settings.DEBUG:
                payload["trace"] = traceback.format_exc()

            return JsonResponse(payload, status=500)