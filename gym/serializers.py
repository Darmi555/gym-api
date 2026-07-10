from rest_framework import serializers

from gym.models import Gym, Studio, Trainer, User, Discipline, TrainingSession, Reservation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password", "email", "phone_number", "date_of_birth", "membership_level"]
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}


    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


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
        fields = ["id", "first_name", "last_name", "experience_years", "description"]


class DisciplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discipline
        fields = ["id", "name", "description"]


class TrainingSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingSession
        fields = ["id", "trainer", "discipline", "studio", "start_time", "end_time"]


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ["id", "user", "training_session"]
