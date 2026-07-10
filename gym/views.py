from django.shortcuts import render
from rest_framework import viewsets

from gym.models import Gym
from gym.serializers import GymSerializer


class GymViewSet(viewsets.ModelViewSet):
    queryset = Gym.objects.all()
    serializer_class = GymSerializer
