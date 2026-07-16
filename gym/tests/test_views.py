from datetime import time

from rest_framework.test import APITestCase
from rest_framework import status

from django.contrib.auth import get_user_model

from gym.models import Gym

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





class UnauthenticatedReservationApiTest(APITestCase):
    def test_auth_required(self):
        response = self.client.get("/api/gym/reservations/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
