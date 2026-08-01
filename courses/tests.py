from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status

from teachers.models import Teacher
from .models import Course


class CourseAPITest(APITestCase):

    def setUp(self):
        user = User.objects.create_user(
            username="teacher",
            password="password123"
        )

        self.client.login(
            username="teacher",
            password="password123"
        )

        teacher = Teacher.objects.create(
            user=user,
            employee_number="EMP001",
            department="Computer Science"
        )

        Course.objects.create(
            course_name="Python",
            course_code="CSC101",
            teacher=teacher
        )

    def test_get_courses(self):
        response = self.client.get("/api/courses/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)