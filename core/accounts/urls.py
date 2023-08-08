from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('login',views.LoginUser.as_view(),name = 'login-view'),
    path('register',views.RegisterUser.as_view(),name = 'register-view'),
    path('logout',views.LogoutUser.as_view(),name = 'logout-view')
]