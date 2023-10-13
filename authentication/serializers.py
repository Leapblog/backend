from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from authentication.models import Profile, User


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

    def validate_type(self, value: str) -> str:
        allowed_types = ["user", "lspp"]

        if value not in allowed_types:
            raise serializers.ValidationError(
                "Invalid user type. Allowed types are: user, lspp"
            )

        return value

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


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")

    class Meta:
        model = Profile
        fields = "__all__"

    # Override for user fields (writable dotted)

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})
        user = instance.user
        user_fields = ["first_name", "last_name", "username"]
        for field in user_fields:
            if field in user_data:
                setattr(user, field, user_data[field])

        user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


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
