from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = "accounts"

urlpatterns = [
    path('login',views.LoginUser.as_view(),name = 'login-view'),
    path('register',views.RegisterUser.as_view(),name = 'register-view'),
    path('logout',LogoutView.as_view(next_page="/"),name = 'logout-view')
 ]