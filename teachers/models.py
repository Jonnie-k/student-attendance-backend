from django.db import models
from django.contrib.auth.models import User

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)#This means that a user can only have one teacher profile...
    employee_number = models.CharField(max_length=20, unique=True)#CharField is used to store text data, and unique=True ensures that each employee number is unique across all teacher records.
    department = models.CharField(max_length=30)#CharField is used to store text data,department where the teacher belongs, and max_length=30 sets the maximum length for the department field.

    def __str__(self):
        return self.user.get_full_name() or self.user.username   #This method defines how the Teacher object will be represented as a string. It returns the full name of the associated user if available; otherwise, it returns the username.
    
