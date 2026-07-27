from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status

from students.models import Student
from teachers.models import Teacher
from courses.models import Course
from .models import Attendance


class AttendanceAPITest(APITestCase):

    def setUp(self):
        user = User.objects.create_user(
            username="student",
            password="password123"
        )

        teacher_user = User.objects.create_user(
            username="teacher",
            password="password123"
        )

        self.client.login(
            username="student",
            password="password123"
        )

        student = Student.objects.create(
            user=user,
            admission_number="ADM001",
            phone_number="0712345678",
            gender="Male"
        )

        teacher = Teacher.objects.create(
            user=teacher_user,
            employee_number="EMP001",
            department="Computer Science"
        )

        course = Course.objects.create(
            course_name="Python",
            course_code="CSC101",
            teacher=teacher
        )

        Attendance.objects.create(
            student=student,
            course=course,
            date="2026-07-23",
            status="Present"
        )

    def test_get_attendance(self):
        response = self.client.get("/api/attendance/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)