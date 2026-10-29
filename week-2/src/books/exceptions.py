from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    response = drf_exception_handler(exc, context)

    if response is None:
        return Response(
            {
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "Internal server error",
                "details": str(exc),
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    details = response.data
    if isinstance(details, dict) and "detail" in details and len(details) == 1:
        message = str(details["detail"])
        details = None
    else:
        message = "Request failed"

    response.data = {
        "code": response.status_code,
        "message": message,
        "details": details,
    }
    return response
