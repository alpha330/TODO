from django.urls import path
from . import views
from rest_framework.authtoken.views import ObtainAuthToken

app_name = "api-v1"
urlpatterns = [
    # Registration API urls
    path("registration/",views.RegistrationApiView.as_view(),name="registration"),
    # Change Password Urls Configs
    # Reset Password Urls Topology
    # Login Token 
    path("token/login/",ObtainAuthToken.as_view(),name="token-login"),
    # Login jwt
]
