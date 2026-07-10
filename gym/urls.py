from rest_framework.routers import DefaultRouter

from gym.views import GymViewSet

router = DefaultRouter()
router.register("gyms", GymViewSet)

urlpatterns = router.urls
