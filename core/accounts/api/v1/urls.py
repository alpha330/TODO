from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

# from rest_framework.authtoken.views import ObtainAuthToken

app_name = "api-v1"
urlpatterns = [
    # Registration API urls
    path(
        "registration/",
        views.RegistrationApiView.as_view(),
        name="registration",
    ),
    #  Activation
    path(
        "activation/confirm/<str:token>",
        views.ConfirmationApiView.as_view(),
        name="activation",
    ),
    # Resend Activation
    path(
        "activation/reconfirm/",
        views.ReconfirmationApiView.as_view(),
        name="reconfirmation",
    ),
    # Change Password Urls Configs
    path(
        "change-password/",
        views.ChangePasswordApiView.as_view(),
        name="change-password",
    ),
    # Reset Password Urls Topology
    path(
        "send-reset-password-link/",
        views.ResetLinkPasswordSendApiView.as_view(),
        name="send-reset-password-link",
    ),
    path(
        "reset-password/<str:token>",
        views.ResetPasswordApiView.as_view(),
        name="reset-password",
    ),
    # Login-Logout Token
    path("token/login/", views.CustomAuthToken.as_view(), name="token-login"),
    path(
        "token/logout/",
        views.CustomDiscardAuthToken.as_view(),
        name="token-logout",
    ),
    # Login jwt
    path(
        "jwt/create/",
        views.CustomTokenObtainPairView.as_view(),
        name="create-jwt-token",
    ),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="refresh-jwt-token"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="verify-jwt-token"),
]
