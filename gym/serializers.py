from rest_framework import serializers

from gym.models import Gym, Studio, Trainer


class GymSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gym
        fields = ["id", "name", "description", "location", "open_time", "close_time"]


class StudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Studio
        fields = ["id", "name", "gym", "capacity"]


class TrainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trainer
        fields = ["id", "name", "gym", "experience_years"]
