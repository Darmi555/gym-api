from rest_framework import viewsets

from gym.models import Gym, Studio
from gym.serializers import GymSerializer, StudioSerializer


class GymViewSet(viewsets.ModelViewSet):
    queryset = Gym.objects.all()
    serializer_class = GymSerializer


class StudioViewSet(viewsets.ModelViewSet):
    queryset = Studio.objects.all()
    serializer_class = StudioSerializer
