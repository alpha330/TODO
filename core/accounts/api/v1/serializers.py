from rest_framework import serializers
from accounts.models import Users
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


# Serializer Api section for lead Api view classes to handel models
class RegistrationSerializer(serializers.ModelSerializer):
    """
    This class is used to serialize
    the User model in order to
    create a new user instance
    """

    password_1 = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = Users
        fields = ["email", "password", "password_1"]

    def validate(self, attrs):
        """
        This method is used to validate
        the password and password
        confirmation fields
        """
        if attrs.get("password") != attrs.get("password_1"):
            raise serializers.ValidationError(
                {"detail": "Password dose not match"}
            )
        try:
            validate_password(attrs["password"])
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": e.messages})

        return super().validate(attrs)

    def create(self, validated_data):
        """
        This method is used
        to create an instance of
        the User model using
        validated data
        """
        validated_data.pop("password_1")
        return Users.objects.create_user(**validated_data)


class CustomAuthTokenSerializer(serializers.Serializer):
    """
    This class is used
    to serialize the
    User model in order to
    create a new user instance
    """

    email = serializers.CharField(label=_("email"), write_only=True)
    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )
    token = serializers.CharField(label=_("Token"), read_only=True)

    def validate(self, attrs):
        """
        Validate and authenticate the user.
        """
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(
                request=self.context.get("request"),
                email=email,
                password=password,
            )

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg, code="authorization")
            if not user.is_verified:
                msg = _("Your account has not been Verified ")
                raise serializers.ValidationError(msg, code="Activation")
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    This class is used
    to serialize the User model
    in order to create a
    new user instance
    """

    def validate(self, attrs):
        """
        Validate and authenticate the user.
        """
        validated_data = super().validate(attrs)
        if not self.user.is_verified:
            msg = _("Your account has not been Verified ")
            raise serializers.ValidationError(msg, code="Activation")
        validated_data["email"] = self.user.email
        validated_data["user_id"] = self.user.id
        return validated_data


class ChangePasswordSerializer(serializers.Serializer):
    """
    This class is used
    to serialize the
    User model in order
    to create a
    new user instance
    """

    old_password = serializers.CharField(max_length=255, required=True)
    new_password_1 = serializers.CharField(max_length=255, required=True)
    new_password_2 = serializers.CharField(max_length=255, required=True)

    def validate(self, attrs):
        """
        Validate and authenticate the user.
        """
        if attrs.get("new_password_1") != attrs.get("new_password_2"):
            raise serializers.ValidationError(
                {"detail": "Old_Password dose not match"}
            )
        try:
            validate_password(attrs["new_password_1"])
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"new_password_1": e.messages})

        return super().validate(attrs)


class ReconfirmationApiSerializer(serializers.Serializer):
    """
    This class is used
    to serialize the
    User model in order
    to create a
    new user instance
    """

    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        """
        Validate and authenticate the user.
        """
        email = attrs.get("email")
        try:
            user_obj = Users.objects.get(email=email)
        except Users.DoesNotExist:
            raise serializers.ValidationError(
                {"detail": "email dose not exist"}
            )
        if user_obj.is_verified:
            raise serializers.ValidationError(
                {"detail": "User was verified before"}
            )
        attrs["user"] = user_obj
        return super().validate(attrs)


class PasswordResetLinkSerializer(serializers.Serializer):
    """
    This class is used to
    serialize the User model
    in order to create a
    new user instance
    """

    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        """
        Validate and authenticate the user.
        """
        email = attrs.get("email")
        try:
            user_obj = Users.objects.get(email=email)
        except Users.DoesNotExist:
            raise serializers.ValidationError(
                {"detail": "email dose not exist"}
            )
        attrs["user"] = user_obj
        return super().validate(attrs)


class ResetPasswordSerializer(serializers.Serializer):
    """
    This class is used
    to serialize the User model
    in order to create a
    new user instance
    """

    new_password = serializers.CharField(required=True)
    new_password_1 = serializers.CharField(required=True)

    def validate(self, attrs):
        """
        Validate and authenticate the user.
        """
        if attrs.get("new_password") != attrs.get("new_password_1"):
            raise serializers.ValidationError(
                {"detail": "password dose not match"}
            )
        try:
            validate_password(attrs.get("new_password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError(
                {"new_password": list(e.messages)}
            )
        return super().validate(attrs)
