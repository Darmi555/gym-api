from rest_framework.test import APITestCase
from rest_framework import status


class UnauthenticatedReservationApiTest(APITestCase):
    def test_auth_required(self):
        response = self.client.get("/api/gym/reservations/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)