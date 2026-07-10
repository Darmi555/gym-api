from rest_framework import serializers

from gym.models import Gym


class GymSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gym
        fields = ["id", "name", "description", "location", "open_time", "close_time"]
