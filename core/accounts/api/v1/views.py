from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    RegistrationSerializer,
    CustomAuthTokenSerializer,
    CustomTokenObtainPairSerializer,
    ChangePasswordSerializer,
    ReconfirmationApiSerializer,
    PasswordResetLinkSerializer,
    ResetPasswordSerializer,
)
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from mail_templated import EmailMessage
from django.contrib.auth import get_user_model
from ..utils import EmailThread
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError
import jwt
from django.conf import settings

# API-VIEWS can create and
# customize in this section
# relation with models and
# Api serializer and api urls

Users = get_user_model()


class RegistrationApiView(generics.GenericAPIView):
    """
    API that can use for registration for new user and verified
    after confirming with email verification topology
    Register a new user to the system

    """

    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        """
        get require elemnts from user like email
        password and confirmation password
        this def can handle verify serialize related
        to registration and save after that
        and send verification email
        to user
        required elements : "email","password","password1"
        """
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            email = serializer.validated_data["email"]
            data = {email}
            user_obj = get_object_or_404(Users, email=email)
            token = self.get_tokens_for_user(user_obj)
            email_obj = EmailMessage(
                "email/activation_email.tpl",
                {"token": token},
                "admin@admin.com",
                ["email"],
            )
            EmailThread(email_obj).run()
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_tokens_for_user(self, user):
        """
        this def for create manula tokens that
        sends with email verification in url verification
        required element: email user comes from Users Model
        """
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class CustomAuthToken(ObtainAuthToken):
    """
    this class create token from verified and authenticated user
    for login with token system
    """

    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {"token": token.key, "user_id": user.pk, "email": user.email}
        )


class CustomDiscardAuthToken(APIView):
    """
    this view discard the token of loggedin user
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    this class create token from verified and authenticated user
    """

    serializer_class = CustomTokenObtainPairSerializer


class ChangePasswordApiView(generics.GenericAPIView):
    """
    This API View is used to change password of a User
    """

    serializer_class = ChangePasswordSerializer
    Model = Users
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Check Old Password
            if not self.object.check_password(
                serializer.data.get("old_password")
            ):
                return Response(
                    {"old password": "Is Wrong"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # set new password and updates password and save
            self.object.set_password(serializer.data.get("new_password_1"))
            self.object.save()
            return Response(
                {"detail": "password has been update"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConfirmationApiView(APIView):
    """
    This API View is used for confirming email address
    """

    def get(self, request, token, *args, **kwargs):
        try:
            token = jwt.decode(
                token, settings.SECRET_KEY, algorithms=["HS256"]
            )
            user_id = token.get("user_id")

        except ExpiredSignatureError:
            return Response(
                {"details": "Token has been Expire"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except InvalidSignatureError:
            return Response(
                {"details": "Invalid Token Signature"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user_obj = Users.objects.get(pk=user_id)
        if user_obj.is_verified:
            return Response({"detail": "Account Verified before"})
        user_obj.is_verified = True
        user_obj.save()
        return Response({"detail": "Activated Successfully"})


class ReconfirmationApiView(generics.GenericAPIView):
    """
    This API view is used to re-send the verification mail again
    """

    serializer_class = ReconfirmationApiSerializer

    def post(self, request, *args, **kwargs):
        serializer = ReconfirmationApiSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.validated_data["user"]
        token = self.get_tokens_for_user(user_obj)
        email_obj = EmailMessage(
            "email/activation_email.tpl",
            {"token": token},
            "admin@admin.com",
            to=[user_obj.email],
        )
        EmailThread(email_obj).run()
        return Response(
            {"detail": "User Activation Resend Successfully"},
            status=status.HTTP_201_CREATED,
        )

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class ResetLinkPasswordSendApiView(generics.GenericAPIView):
    """
    This API view is used to send reset password link to user
    """

    serializer_class = PasswordResetLinkSerializer

    def post(self, request, *args, **kwargs):
        serializer = PasswordResetLinkSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.validated_data["user"]
        token = self.get_tokens_for_user(user_obj)
        email_obj = EmailMessage(
            "email/reset_password.tpl",
            {"token": token},
            "admin@admin.com",
            to=[user_obj.email],
        )
        EmailThread(email_obj).run()
        return Response(
            {"detail": "Reset Password Link send Successfully"},
            status=status.HTTP_200_OK,
        )

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class ResetPasswordApiView(generics.GenericAPIView):
    """
    This API View is used for resetting the password of a user
    """

    model = Users
    serializer_class = ResetPasswordSerializer

    def put(self, request, token, *args, **kwargs):
        try:
            token = jwt.decode(
                token, settings.SECRET_KEY, algorithms=["HS256"]
            )
            user_id = token.get("user_id")
        except ExpiredSignatureError:
            return Response(
                {"details": "Token has been Expire"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except InvalidSignatureError:
            return Response(
                {"details": "Invalid Token Signature"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        self.object = Users.objects.get(pk=user_id)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(
                {"detail": "new password has been set successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
