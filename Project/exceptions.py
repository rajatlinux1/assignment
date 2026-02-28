import logging

from rest_framework.views import exception_handler

logger = logging.getLogger("Project")


def custom_exception_handler(exc, context):
    """
    Centralized DRF exception handler.
    Intercepts any unhandled or validation errors, logs them properly,
    and formats them consistently for API consumers without leaking HTML 500 stacks.
    """
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if response is not None:
        # Standard validation or DRF error
        custom_response_data = {
            "error": True,
            "message": "Validation or input error.",
            "details": response.data,
        }

        # Log 400s as warnings
        logger.warning(f"API Client Error: {custom_response_data}", exc_info=exc)
        response.data = custom_response_data
    else:
        # Unexpected 500 error thrown upstream
        logger.error(f"Unhandled API Exception in {context.get('view')}", exc_info=exc)

        # We manually construct a 500 JSON response
        from rest_framework.response import Response

        response = Response(
            {
                "error": True,
                "message": "An unexpected server error occurred.",
                "details": str(exc),
            },
            status=500,
        )

    return response
