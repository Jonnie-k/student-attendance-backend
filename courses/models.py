from django.db import models
from teachers.models import Teacher

# Create your models here.
class Course(models.Model):
    course_name = models.CharField(max_length=100)#CharField is used to store text data, and max_length=100 sets the maximum length for the course name.
    course_code = models.CharField(max_length=10, unique=True)#CharField is used to store text data, and unique=True ensures that each course code is unique across all course records.
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="courses")#This creates a foreign key relationship to the Teacher model, indicating that each course is associated with a specific teacher.on_delete=models.CASCADE means that if a teacher is deleted, all their associated courses will also be deleted. related_name="courses" allows you to access the courses taught by a teacher using teacher.courses.   
def __str__(self):
        return f"{self.course_name} ({self.course_code})"   #This method defines how the Course object will be represented as a string. It returns the course name along with its code in parentheses.
