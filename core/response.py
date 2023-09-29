from rest_framework import status
from rest_framework.response import Response


class CustomResponse:
    @staticmethod
    def success(data=None, message="", status_code=status.HTTP_200_OK):
        """
        Custom success response handler for sending success responses.

        Args:
            data: The data to be sent along with the response. Defaults to None.
            message (str): Message to be sent along with the response. Defaults to "".
            status_code (int): Status code of the respone. Defaults to 200.

        Returns:
            Response: A response object with all the aforementioned data.
        """
        return Response(
            data={"success": True, "data": data, "message": message},
            status=status_code,
        )

    @staticmethod
    def error(message="", data=None, status_code=status.HTTP_400_BAD_REQUEST):
        """
        Custom error response handler for sending error responses.

        Args:
            message (str): Message to be sent along with the response. Defaults to "".
            data: The data to be sent along with the response. Defaults to None.
            status_code (int): Status code of the respone. Defaults to 400.

        Returns:
            Response: A response object with all the aforementioned data.
        """
        return Response(
            data={"success": False, "errors": data, "message": message},
            status=status_code,
        )
