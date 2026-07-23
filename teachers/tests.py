from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Teacher


class TeacherAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="teacher",
            password="password123"
        )

        self.client.login(
            username="teacher",
            password="password123"
        )

        Teacher.objects.create(
            user=self.user,
            employee_number="EMP001",
            department="Computer Science"
        )

    def test_get_teachers(self):
        response = self.client.get("/api/teachers/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)