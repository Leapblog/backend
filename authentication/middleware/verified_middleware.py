from django.http import HttpRequest
from rest_framework.exceptions import AuthenticationFailed


class EmailVerificationError(Exception):
    pass


def verified_middleware(get_response):
    def middleware(request: HttpRequest):
        excluded_paths = [
            "/api/auth/verify-otp/",
            "/api/auth/resend-otp/",
        ]

        if not hasattr(request, "user"):
            return get_response(request)

        if request.path_info in excluded_paths:
            return get_response(request)

        response = get_response(request)

        if not request.user.is_active:
            raise EmailVerificationError("Verify your email first!")
        return response

    return middleware
