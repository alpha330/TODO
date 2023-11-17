from django.urls import path,include
from . import views
from django.contrib.auth.views import LogoutView

app_name = "accounts"

urlpatterns = [
    path("",include("django.contrib.auth.urls")),
    path('login',views.LoginUser.as_view(),name = 'login-view'),
    path('register',views.RegisterUser.as_view(),name = 'register-view'),
    path('logout',LogoutView.as_view(next_page="/"),name = 'logout-view'),
    path("api/v1/",include("accounts.api.v1.urls"))
 ]