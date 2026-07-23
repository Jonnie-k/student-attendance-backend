from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Student


class StudentAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword123"
        )

        self.client.login(
            username="testuser",
            password="testpassword123"
        )

        Student.objects.create(
            user=self.user,
            admission_number="ADM001",
            phone_number="0712345678",
            gender="Male"
        )

    def test_get_students(self):
        response = self.client.get("/api/students/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_student_count(self):
        self.assertEqual(Student.objects.count(), 1)