from . import views
from rest_framework.routers import DefaultRouter


# urls configs
app_name = "api_v1"
router = DefaultRouter()
router.register("task", views.TaskModelViewSet, basename="task")

urlpatterns = router.urls
