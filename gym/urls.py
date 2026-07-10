from rest_framework.routers import DefaultRouter

from gym.views import GymViewSet, StudioViewSet, TrainerViewSet

router = DefaultRouter()
router.register("gyms", GymViewSet)
router.register("studios", StudioViewSet)
router.register("trainers", TrainerViewSet)

urlpatterns = router.urls
