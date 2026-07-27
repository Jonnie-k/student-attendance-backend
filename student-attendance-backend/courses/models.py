from django.db import models
from teachers.models import Teacher

# Create your models here.
class Course(models.Model):
    course_name = models.CharField(max_length=100)
    course_code = models.CharField(max_length=10, unique=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="courses")

    def __str__(self):
        return f"{self.course_name} ({self.course_code})"
