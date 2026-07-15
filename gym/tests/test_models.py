from datetime import time, timedelta
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone

from gym.models import Gym, Studio, Trainer, Discipline, TrainingSession, Reservation

User = get_user_model()


class UserManagerTest(TestCase):
    def test_user_create_hashes_password(self):
        user = User.objects.create_user(username="testuser", password="testpassword", email="testemail@gmail.com")
        self.assertEqual(user.email, "testemail@gmail.com")
        self.assertTrue(user.check_password("testpassword"))

    def test_create_superuser_flags(self):
        admin = User.objects.create_superuser(email="admin@example.com", username="admin", password="tajne123")
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)

    def test_default_membership_level(self):
        user = User.objects.create_user(username="testuser", password="testpassword", email="testemail@gmail.com")
        self.assertEqual(user.membership_level, "basic")

    def test_create_user_without_email_raises(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", username="x", password="x12345")


class ModelStrTest(TestCase):
    def setUp(self):
        self.gym = Gym.objects.create(
            name="FitZone", location="Warszawa", open_time=time(6, 0), close_time=time(22, 0)
        )
        self.studio = Studio.objects.create(name="Sala A", gym=self.gym, capacity=10)
        self.trainer = Trainer.objects.create(first_name="Anna", last_name="Kowalska", experience_years=5)
        self.discipline = Discipline.objects.create(name="Yoga")

    def test_gym_str(self):
        self.assertEqual(str(self.gym), "FitZone (Warszawa)")

    def test_studio_str(self):
        self.assertEqual(str(self.studio), "Sala A")

    def test_trainer_str(self):
        self.assertEqual(str(self.trainer), "Anna Kowalska")

    def test_discipline_str(self):
        self.assertEqual(str(self.discipline), "Yoga")

    def test_training_session_str(self):
        session = TrainingSession.objects.create(
            trainer=self.trainer,
            discipline=self.discipline,
            studio=self.studio,
            start_time=timezone.now(),
            end_time=timezone.now() + timedelta(hours=1),
        )
        self.assertIn("Yoga", str(session))


class TrainingSessionTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@test.com", username="tester", password="haslo123")
        self.gym = Gym.objects.create(
            name="FitZone", location="Warszawa", open_time=time(6, 0), close_time=time(22, 0)
        )
        self.studio = Studio.objects.create(name="Sala A", gym=self.gym, capacity=10)
        self.trainer = Trainer.objects.create(first_name="Anna", last_name="Kowalska", experience_years=5)
        self.discipline = Discipline.objects.create(name="Yoga")
        self.training_session = TrainingSession.objects.create(
            trainer=self.trainer,
            discipline=self.discipline,
            studio=self.studio,
            start_time=timezone.now() + timedelta(hours=1),
            end_time=timezone.now() + timedelta(hours=5),
        )

    def test_unique_constraint(self):
        reservation = Reservation.objects.create(
            user=self.user,
            training_session=self.training_session,
        )
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Reservation.objects.create(user=self.user, training_session=self.training_session)
