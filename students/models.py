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
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_number = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)

    def __str__(self):
        return self.user.get_full_name() or self.user.username