from rest_framework.response import Response
from rest_framework.views import exception_handler

from core.response import CustomResponse


def handle_other_exceptions(exc: Exception, context):
    """
    Handle all other exceptions that Django Rest Framework (DRF) does not handle.

    Args:
        exc (Exception): The exception that was raised.
        context (Dict): The context of the exception.

    Returns:
        Response: A DRF Response object with a 500 status code and a JSON payload
        containing the exception message.
    """
    headers = {}
    data = {"detail": str(exc)}
    return Response(data, status=500, headers=headers)


def custom_exception_handler(exc, context):
    """
    Custom exception handler for handling exceptions raised in Django views.

    Args:
        exc (Exception): The exception that was raised.
        context (Dict[str, Any]): The context of the exception.

    Returns:
        CustomResponse: A custom response object with error details.
    """
    response = exception_handler(exc, context)

    if response is None:
        response = handle_other_exceptions(exc, context)

    return CustomResponse.error(
        message=response.status_text,
        data=response.data,
        status_code=response.status_code,
    )
