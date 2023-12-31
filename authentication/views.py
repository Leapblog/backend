from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import BlackListedToken, Profile
from authentication.serializers import (
    LoginSerializer,
    OtpSerializer,
    ProfileSerializer,
    RefreshTokenSerializer,
    RegisterSerializer,
)
from authentication.utils import generate_otp, send_otp_email
from core.response import CustomResponse as cr

from .authentication import JWTAuthentication as jwt_auth

User = get_user_model()


class RegisterView(APIView):
    serializer_class = RegisterSerializer

    def post(self, request: Request) -> Response:
        """
        Register a new user with the given request data.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: The HTTP response object containing the access and refresh tokens.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data.pop("confirm_password")
        user = serializer.save()
        if settings.ENV == "production":
            user.is_active = False
            otp = generate_otp()
            user.otp = otp
            send_otp_email(user.email, otp)

            user.save()

        access_token, refresh_token = jwt_auth.create_tokens(user)
        return cr.success(
            data={"access_token": access_token, "refresh_token": refresh_token},
            message="User registered successfully!",
            status_code=status.HTTP_201_CREATED,
        )


class VerifyOtpView(APIView):
    serializer_class = OtpSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        """
        Verifies the OTP sent to the user

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: The HTTP response object containing the success message.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.filter(pk=request.user.id).first()
        if not user:
            return cr.error("User not found!")

        if user.is_active:
            return cr.error("User is already verified!")

        if int(user.otp) != serializer.validated_data.get("otp"):
            return cr.error("OTP doesn't match!")

        user.is_active = True
        user.otp = ""
        user.save()

        return cr.success(message="OTP verified successfully!")


class ResendOtpView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Request:
        """
        Resends the OTP to the user's email for verification

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: The HTTP response object containing the success message.
        """
        user = User.objects.filter(pk=request.user.id).first()
        if not user:
            return cr.error("User not found!")

        if user.is_active:
            return cr.error("User is already verified!")

        otp = generate_otp()
        send_otp_email(user.email, otp)

        user.otp = otp
        user.save()

        return cr.success(message="OTP resent successfully!")


class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request: Request) -> Response:
        """
        Logs in a user with the provided email and password.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: The HTTP response object containing the access and refresh tokens.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")

        user = User.objects.filter(email=email).first()
        if not user or not user.check_password(password):
            return cr.error(
                message="Invalid credentials provided",
                status_code=status.HTTP_403_FORBIDDEN,
            )
        access_token, refresh_token = jwt_auth.create_tokens(user)

        return cr.success(
            data={"access_token": access_token, "refresh_token": refresh_token},
            message="User logged in successfully!",
        )


class RefreshTokenView(APIView):
    serializer_class = RefreshTokenSerializer

    def post(self, request: Request) -> Response:
        """
        Refreshes the access token using the provided refresh token.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: The HTTP response object containing the new access token.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        access_token = jwt_auth.refresh_access_token(
            serializer.validated_data.get("refresh_token")
        )

        return cr.success(
            data={"access_token": access_token},
            message="Access token refreshed successfully!",
        )


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get(self, request: Request) -> Response:
        """
        Get the profile associated with the authenticated user.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: The HTTP response object containing the new access token.
        """
        profile = Profile.objects.filter(user=request.user).first()
        serializer = self.serializer_class(instance=profile)
        return cr.success(data=serializer.data, message="Profile fetched successfully!")

    def put(self, request: Request) -> Response:
        """
        Create and update a profile for the authenticated user.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: The HTTP response object containing the new access token.
        """
        profile = Profile.objects.filter(user=request.user).first()
        serializer = self.serializer_class(
            instance=profile, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
        return cr.success(data=serializer.data, message="Profile created successfully.")


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        """
        Logs out the user by blacklisting the token.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: The HTTP response object.
        """
        BlackListedToken.objects.create(token=request.auth)
        return cr.success(message="User logged out successfully!")
