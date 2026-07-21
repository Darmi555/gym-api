from django.utils import timezone
from datetime import timedelta
from rest_framework.test import APITestCase
from rest_framework import status

from django.contrib.auth import get_user_model

from gym.models import Gym, Trainer, Discipline, Studio, TrainingSession, Reservation

User = get_user_model()

class UserRegistrationApiTest(APITestCase):
    def test_registration_creates_user_and_hides_password(self):
        response = self.client.post(
            "/api/gym/users/",
            data={
                "email": "test@test.com",
                "password": "testpassowrd",
                "username": "testuser",
            }
        )
        user = User.objects.get(email="test@test.com")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(user.email, "test@test.com")
        self.assertTrue(user.check_password("testpassowrd"))
        self.assertNotIn("password", response.data)


class GymApiTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="user@test.com", username="user", password="pass12345"
        )
        self.admin = User.objects.create_superuser(
            email="admin@test.com", username="admin", password="pass12345"
        )
        self.gym = Gym.objects.create(
            name="testgym",
            description="testgym description",
            location="testgym location",
            open_time="10:00",
            close_time="20:00",
        )

    def test_gym_unauthorized_user(self):
        response = self.client.get("/api/gym/gyms/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        names = [gym["name"] for gym in response.data["results"]]
        self.assertIn("testgym", names)

    def test_gym_create_gym_unauthorized_user(self):
        self.client.force_authenticate(self.user)
        response = self.client.post("/api/gym/gyms/", data={"name": "testgym2"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Gym.objects.count(), 1)

    def test_gym_create_admin_user(self):
        self.client.force_authenticate(self.admin)
        response = self.client.post(
            "/api/gym/gyms/",
            data={
                "name": "testgym2",
                "location": "loc",
                "open_time": "08:00",
                "close_time": "22:00",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Gym.objects.count(), 2)


class TrainerAPiTest(APITestCase):
    def setUp(self):
        self.trainer1 = Trainer.objects.create(
            first_name="test1",
            last_name="test2",
            experience_years=7
        )
        self.trainer2 = Trainer.objects.create(
            first_name="test2",
            last_name="test3",
            experience_years=5
        )
        self.discipline = Discipline.objects.create(
            name="testdiscipline",
        )
        self.gym = Gym.objects.create(
            name="testgym",
            description="testgym description",
            location="testgym location",
            open_time="10:00",
            close_time="20:00",
        )
        self.studio = Studio.objects.create(
            name="teststudio",
            description="teststudio description",
            gym=self.gym,
            capacity=30,
        )
        self.trainingsession1 = TrainingSession.objects.create(
            trainer=self.trainer1,
            discipline=self.discipline,
            studio=self.studio,
            start_time=timezone.now() + timedelta(hours=1),
            end_time=timezone.now() + timedelta(hours=5),
        )
        self.trainingsession2 = TrainingSession.objects.create(
            trainer=self.trainer2,
            discipline=self.discipline,
            studio=self.studio,
            start_time=timezone.now() + timedelta(hours=2),
            end_time=timezone.now() + timedelta(hours=7),
        )

    def test_trainer_custom_action_endpoint(self):
        response = self.client.get(f"/api/gym/trainers/{self.trainer1.id}/sessions/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["trainer"], str(self.trainer1))
        response = self.client.get(f"/api/gym/trainers/{self.trainer2.id}/sessions/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["trainer"], str(self.trainer2))


class TrainingSessionTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="user@test.com", username="user", password="pass12345"
        )
        self.admin = User.objects.create_superuser(
            email="admin@test.com", username="admin", password="pass12345"
        )
        self.discipline = Discipline.objects.create(
            name="testdiscipline",
        )
        self.discipline2 = Discipline.objects.create(
            name="testdiscipline2",
        )
        self.trainer = Trainer.objects.create(
            first_name="test_first",
            last_name="test_last",
            experience_years=10
        )
        self.gym = Gym.objects.create(
            name="testgym",
            description="testgym description",
            location="testgym location",
            open_time="10:00",
            close_time="20:00",
        )
        self.studio = Studio.objects.create(
            name="teststudio",
            description="teststudio description",
            gym=self.gym,
            capacity=30,
        )

    def test_training_session_validate_method_create_in_past(self):
        self.client.force_authenticate(self.admin)
        response = self.client.post(
            "/api/gym/training-sessions/",
            data={
                "trainer": self.trainer.id,
                "discipline": self.discipline.id,
                "studio": self.studio.id,
                "start_time": timezone.now() - timedelta(hours=1),
                "end_time": timezone.now() + timedelta(hours=5),
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_training_session_validate_method_end_earlier_than_start_time(self):
        self.client.force_authenticate(self.admin)
        response = self.client.post(
            "/api/gym/training-sessions/",
            data={
                "trainer": self.trainer.id,
                "discipline": self.discipline.id,
                "studio": self.studio.id,
                "start_time": timezone.now() + timedelta(hours=5),
                "end_time": timezone.now() + timedelta(hours=2),
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_training_session_validate_method_correct_way(self):
        self.client.force_authenticate(self.admin)
        response = self.client.post(
            "/api/gym/training-sessions/",
            data={
                "trainer": self.trainer.id,
                "discipline": self.discipline.id,
                "studio": self.studio.id,
                "start_time": timezone.now() + timedelta(hours=2),
                "end_time": timezone.now() + timedelta(hours=5),
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_training_session_filtr_by_discipline(self):
        now = timezone.now()
        training_session1 = TrainingSession.objects.create(
            trainer=self.trainer,
            discipline=self.discipline,
            studio=self.studio,
            start_time=now + timedelta(hours=2),
            end_time=now + timedelta(hours=5),
        )
        training_session2 = TrainingSession.objects.create(
            trainer=self.trainer,
            discipline=self.discipline2,
            studio=self.studio,
            start_time=now + timedelta(hours=4),
            end_time=now + timedelta(hours=6),

        )
        response = self.client.get(f"/api/gym/training-sessions/?discipline={self.discipline.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["discipline"], str(self.discipline))
        response = self.client.get(f"/api/gym/training-sessions/?discipline={self.discipline2.id}")
        self.assertEqual(response.data["results"][0]["discipline"], str(self.discipline2))

    def test_training_session_filtr_by_date(self):
        now = timezone.now()
        training_session1 = TrainingSession.objects.create(
            trainer=self.trainer,
            discipline=self.discipline,
            studio=self.studio,
            start_time=now,
            end_time=now + timedelta(days=5),
        )
        training_session2 = TrainingSession.objects.create(
            trainer=self.trainer,
            discipline=self.discipline2,
            studio=self.studio,
            start_time=now + timedelta(days=2),
            end_time=now + timedelta(days=6)
        )
        response = self.client.get(f"/api/gym/training-sessions/?date={now.date()}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_training_session_available_places(self):
        now = timezone.now()
        training_session1 = TrainingSession.objects.create(
            trainer=self.trainer,
            discipline=self.discipline,
            studio=self.studio,
            start_time=now,
            end_time=now + timedelta(days=5),
        )
        response = self.client.get(f"/api/gym/training-sessions/{training_session1.id}/")
        self.assertEqual(response.data["available_places"], 30)
        reservation = Reservation.objects.create(
            user=self.user,
            training_session=training_session1,
        )
        response = self.client.get(f"/api/gym/training-sessions/{training_session1.id}/")
        self.assertEqual(response.data["available_places"], 29)


class ReservationApiTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="user@test.com", username="user", password="pass12345"
        )
        self.admin = User.objects.create_superuser(
            email="admin@test.com", username="admin", password="pass12345"
        )
        self.discipline = Discipline.objects.create(
            name="testdiscipline",
        )
        self.discipline2 = Discipline.objects.create(
            name="testdiscipline2",
        )
        self.trainer = Trainer.objects.create(
            first_name="test_first",
            last_name="test_last",
            experience_years=10
        )
        self.gym = Gym.objects.create(
            name="testgym",
            description="testgym description",
            location="testgym location",
            open_time="10:00",
            close_time="20:00",
        )

    def test_create_reservation_with_success(self):
        self.client.force_authenticate(self.user)
        now = timezone.now() + timedelta(hours=1)
        studio = Studio.objects.create(
            name="teststudio",
            description="teststudio description",
            gym=self.gym,
            capacity=30,
        )
        training_session = TrainingSession.objects.create(
            trainer=self.trainer,
            discipline=self.discipline,
            studio=studio,
            start_time=now,
            end_time=now + timedelta(days=5),
        )
        response = self.client.post("/api/gym/reservations/",data={
                "training_session":training_session.id,
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reservation.objects.count(), 1)
        reservation = Reservation.objects.first()
        self.assertEqual(reservation.user, self.user)

    def test_create_reservation_with_no_available_places(self):
        self.client.force_authenticate(self.user)
        now = timezone.now() + timedelta(hours=1)
        studio = Studio.objects.create(
            name="teststudio",
            description="teststudio description",
            gym=self.gym,
            capacity=0,
        )
        training_session = TrainingSession.objects.create(
            trainer=self.trainer,
            discipline=self.discipline,
            studio=studio,
            start_time=now,
            end_time=now + timedelta(days=5),
        )
        response = self.client.post("/api/gym/reservations/",data={
                "training_session":training_session.id,
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Reservation.objects.count(), 0)

    def test_create_double_reservation(self):
        self.client.force_authenticate(self.user)
        now = timezone.now() + timedelta(hours=1)
        studio = Studio.objects.create(
            name="teststudio",
            description="teststudio description",
            gym=self.gym,
            capacity=5,
        )
        training_session = TrainingSession.objects.create(
            trainer=self.trainer,
            discipline=self.discipline,
            studio=studio,
            start_time=now,
            end_time=now + timedelta(days=5),
        )
        response = self.client.post("/api/gym/reservations/",data={
                "training_session":training_session.id,
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reservation.objects.count(), 1)
        response = self.client.post("/api/gym/reservations/",data={
                "training_session":training_session.id,
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Reservation.objects.count(), 1)

    def test_create_reservation_in_past(self):
        self.client.force_authenticate(self.user)
        now = timezone.now() - timedelta(hours=1)
        studio = Studio.objects.create(
            name="teststudio",
            description="teststudio description",
            gym=self.gym,
            capacity=5,
        )
        training_session = TrainingSession.objects.create(
            trainer=self.trainer,
            discipline=self.discipline,
            studio=studio,
            start_time=now,
            end_time=now + timedelta(days=5),
        )
        response = self.client.post("/api/gym/reservations/",data={
                "training_session":training_session.id,
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Reservation.objects.count(), 0)

    def test_reservation_list_shows_only_own(self):
        now = timezone.now() + timedelta(hours=1)
        studio = Studio.objects.create(
            name="teststudio",
            description="teststudio description",
            gym=self.gym,
            capacity=5,
        )
        training_session = TrainingSession.objects.create(
            trainer=self.trainer,
            discipline=self.discipline,
            studio=studio,
            start_time=now,
            end_time=now + timedelta(days=5),
        )
        user2 = User.objects.create_user(
            email="user2@test.com", username="user2", password="pass12345"
        )
        Reservation.objects.create(user=self.user, training_session=training_session)
        Reservation.objects.create(user=user2, training_session=training_session)
        self.client.force_authenticate(self.user)
        response = self.client.get("/api/gym/reservations/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["user"], self.user.username)


