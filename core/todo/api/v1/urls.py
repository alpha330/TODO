from . import views
from rest_framework.routers import DefaultRouter
from django.urls import path, include

# urls configs
app_name = "api_v1"
router = DefaultRouter()
router.register("task", views.TaskModelViewSet, basename="task")
urlpatterns = [
    path("live/weather/", views.CurrentWeather.as_view(), name="live-weather"),
    path("live/crypto/", views.CurrentCryptoPrice.as_view(), name="live-crypto"),
    path("api/v1/", include(router.urls)),
]
