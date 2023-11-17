from django.urls import path
from . import views

app_name = "api-v1"
urlpatterns = [
    # Registration API urls
    path("registration/",views.RegistrationApiView.as_view(),name="registration")
    # Change Password Urls Configs
    # Reset Password Urls Topology
    # Login Token 
    # Login jwt
]
