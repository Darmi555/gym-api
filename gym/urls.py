from rest_framework.routers import DefaultRouter

from gym.views import GymViewSet, StudioViewSet

router = DefaultRouter()
router.register("gyms", GymViewSet)
router.register("studios", StudioViewSet)

urlpatterns = router.urls
