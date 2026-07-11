from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

from gym.models import Gym, Studio, Trainer, User, Discipline, TrainingSession, Reservation
from gym.permissions import IsAdminOrReadOnly
from gym.serializers import GymSerializer, StudioSerializer, TrainerSerializer, UserSerializer, DisciplineSerializer, \
    TrainingSessionSerializer, ReservationSerializer, ReservationListSerializer, StudioListSerializer, \
    TrainingSessionListSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)


class GymViewSet(viewsets.ModelViewSet):
    queryset = Gym.objects.all()
    serializer_class = GymSerializer
    permission_classes = [IsAdminOrReadOnly]


class StudioViewSet(viewsets.ModelViewSet):
    queryset = Studio.objects.all()
    serializer_class = StudioSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return StudioListSerializer
        return StudioSerializer


class TrainerViewSet(viewsets.ModelViewSet):
    queryset = Trainer.objects.all()
    serializer_class = TrainerSerializer
    permission_classes = [IsAdminOrReadOnly]


class DisciplineViewSet(viewsets.ModelViewSet):
    queryset = Discipline.objects.all()
    serializer_class = DisciplineSerializer
    permission_classes = [IsAdminOrReadOnly]


class TrainingSessionViewSet(viewsets.ModelViewSet):
    queryset = TrainingSession.objects.all()
    serializer_class = TrainingSessionSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return TrainingSessionListSerializer
        return TrainingSessionSerializer

    def get_queryset(self):
        queryset = TrainingSession.objects.all()
        dicipline_id = self.request.query_params.get("discipline")
        date = self.request.query_params.get("date")

        if dicipline_id:
            queryset = queryset.filter(discipline_id=dicipline_id)
        if date:
            queryset = queryset.filter(start_time__date=date)

        return queryset


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return ReservationListSerializer
        return ReservationSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Reservation.objects.all()
        return Reservation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
