from rest_framework import viewsets

from gym.models import Gym, Studio, Trainer, User, Discipline, TrainingSession, Reservation
from gym.serializers import GymSerializer, StudioSerializer, TrainerSerializer, UserSerializer, DisciplineSerializer, \
    TrainingSessionSerializer, ReservationSerializer, ReservationListSerializer, StudioListSerializer, \
    TrainingSessionListSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GymViewSet(viewsets.ModelViewSet):
    queryset = Gym.objects.all()
    serializer_class = GymSerializer


class StudioViewSet(viewsets.ModelViewSet):
    queryset = Studio.objects.all()
    serializer_class = StudioSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return StudioListSerializer
        return StudioSerializer


class TrainerViewSet(viewsets.ModelViewSet):
    queryset = Trainer.objects.all()
    serializer_class = TrainerSerializer


class DisciplineViewSet(viewsets.ModelViewSet):
    queryset = Discipline.objects.all()
    serializer_class = DisciplineSerializer


class TrainingSessionViewSet(viewsets.ModelViewSet):
    queryset = TrainingSession.objects.all()
    serializer_class = TrainingSessionSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return TrainingSessionListSerializer
        return TrainingSessionSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return ReservationListSerializer
        return ReservationSerializer
