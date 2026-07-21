from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):#This creates a new model called Student, which will be used to store information about students in the database.
    GENDER_CHOICES = [#This defines a list of tuples that will be used to provide choices for the gender field in the Student model
        ("Male", "Male"),
        ("Female", "Female"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)#This means that a user can only have one student profile...
    admission_number = models.CharField(max_length=20, unique=True)#CharField is used to store text data, and unique=True ensures that each admission number is unique across all student records.
    phone_number = models.CharField(max_length=15)#CharField is used to store text data, and max_length=15 sets the maximum length for the phone number.
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)#CharField is used to store text data, and choices=GENDER_CHOICES restricts the values to the predefined gender options.
    def __str__(self):
        return self.user.get_full_name() or self.user.username   #This method defines how the Student object will be represented as a string. It returns the full name of the associated user if available; otherwise, it returns the username.
    

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)#This means that a user can only have one teacher profile...
    employee_number = models.CharField(max_length=20, unique=True)#CharField is used to store text data, and unique=True ensures that each employee number is unique across all teacher records.
    department = models.CharField(max_length=30)#CharField is used to store text data,department where the teacher belongs, and max_length=30 sets the maximum length for the department field.

    def __str__(self):
        return self.user.get_full_name() or self.user.username   #This method defines how the Teacher object will be represented as a string. It returns the full name of the associated user if available; otherwise, it returns the username.
    

class Course(models.Model):
    course_name = models.CharField(max_length=100)#CharField is used to store text data, and max_length=100 sets the maximum length for the course name.
    course_code = models.CharField(max_length=10, unique=True)#CharField is used to store text data, and unique=True ensures that each course code is unique across all course records.
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="courses")#This creates a foreign key relationship to the Teacher model, indicating that each course is associated with a specific teacher.on_delete=models.CASCADE means that if a teacher is deleted, all their associated courses will also be deleted. related_name="courses" allows you to access the courses taught by a teacher using teacher.courses.   
def __str__(self):
        return f"{self.course_name} ({self.course_code})"   #This method defines how the Course object will be represented as a string. It returns the course name along with its code in parentheses.