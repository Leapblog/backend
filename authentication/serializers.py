from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from authentication.models import User


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()


class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField()
    type = serializers.CharField(default="user")

    class Meta:
        model = User
        fields = ("email", "username", "password", "confirm_password", "type")

    def create(self, validated_data: dict) -> User:
        """
        Create a new user with the given validated data.

        Args:
            validated_data (dict): The validated data for the new user.

        Returns:
            User: The newly created user.
        """
        password = validated_data.pop("password")
        validated_data["password"] = make_password(password)
        user = super(RegisterSerializer, self).create(validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "type",
        )


class OtpSerializer(serializers.Serializer):
    otp = serializers.IntegerField()
