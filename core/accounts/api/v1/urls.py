from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
# from rest_framework.authtoken.views import ObtainAuthToken

app_name = "api-v1"
urlpatterns = [
    # Registration API urls
    path("registration/",views.RegistrationApiView.as_view(),name="registration"),
    # Change Password Urls Configs
    # Reset Password Urls Topology
    # Login-Logout Token 
    path("token/login/",views.CustomAuthToken.as_view(),name="token-login"),
    path("token/logout/",views.CustomDiscardAuthToken.as_view(),name="token-logout"),
    # Login jwt
    path("jwt/create/",TokenObtainPairView.as_view(),name="create-jwt-token"),
    path("jwt/refresh/",TokenRefreshView.as_view(),name="refresh-jwt-token"),
    path("jwt/verify/",TokenVerifyView.as_view(),name="verify-jwt-token")
]
