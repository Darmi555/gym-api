from rest_framework.routers import DefaultRouter

from gym.views import GymViewSet, StudioViewSet, TrainerViewSet, ReservationViewSet, TrainingSessionViewSet, \
    DisciplineViewSet, UserViewSet

router = DefaultRouter()
router.register("users", UserViewSet)
router.register("gyms", GymViewSet)
router.register("studios", StudioViewSet)
router.register("trainers", TrainerViewSet)
router.register("disciplines", DisciplineViewSet)
router.register("training-sessions", TrainingSessionViewSet)
router.register("reservations", ReservationViewSet)

urlpatterns = router.urls
