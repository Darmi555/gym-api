from rest_framework.test import APITestCase
from rest_framework import status

from django.contrib.auth import get_user_model


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


class UnauthenticatedReservationApiTest(APITestCase):
    def test_auth_required(self):
        response = self.client.get("/api/gym/reservations/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
