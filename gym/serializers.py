from django.utils import timezone

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


class StudioListSerializer(serializers.ModelSerializer):
    gym = serializers.CharField(source="gym.__str__", read_only=True)

    class Meta:
        model = Studio
        fields = ["id","name", "gym", "description"]


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

class TrainingSessionListSerializer(serializers.ModelSerializer):
    trainer = serializers.CharField(source="trainer.__str__", read_only=True)
    discipline = serializers.CharField(source="discipline.__str__", read_only=True)
    studio = serializers.CharField(source="studio.__str__", read_only=True)
    start_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    end_time = serializers.DateTimeField(format="%H:%M")
    available_places = serializers.SerializerMethodField()

    def get_available_places(self, obj):
        return obj.studio.capacity - obj.reservations.count()

    class Meta:
        model = TrainingSession
        fields = ["id", "trainer", "discipline", "studio", "start_time", "end_time", "available_places"]


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ["id", "user", "training_session"]
        read_only_fields = ["user"]

    def validate(self, attrs):
        training_session = attrs["training_session"]
        user = self.context["request"].user

        reservation_count = Reservation.objects.filter(training_session=training_session).count()
        if reservation_count >= training_session.studio.capacity:
            raise serializers.ValidationError("Brak wolnych miejsc")
        if Reservation.objects.filter(user=user, training_session=training_session).exists():
            raise serializers.ValidationError("Posiadasz już zarezerwowaną sesję na te zajęcia")
        if training_session.start_time < timezone.now():
            raise serializers.ValidationError("Zajęcią już sie odbyły")
        return attrs


class ReservationListSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    training_session = serializers.CharField(source="training_session.__str__", read_only=True)

    class Meta:
        model = Reservation
        fields = ["id", "user", "training_session"]

