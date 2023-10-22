from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter


#urls configs
app_name = "api_v1"
router = DefaultRouter()
router.register('post', views.TaskModelViewSet, basename='post')

urlpatterns = router.urls