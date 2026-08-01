from django.db import models
from students.models import Student
from courses.models import Course


class Attendance(models.Model):
    STATUS_CHOICES = [#This defines a list of tuples that will be used to provide choices for the status field in the Attendance model.
        ("Present", "Present"),
        ("Absent", "Absent"),
        ("Late", "Late"),
    ]

    student = models.ForeignKey(#This creates a foreign key relationship to the Student model, indicating that each attendance record is associated with a specific student.
        Student,
        on_delete=models.CASCADE,#This means that if a student is deleted, all their associated attendance records will also be deleted.
        related_name="attendance_records"#This means that you can access the attendance records of a student using student.attendance_records
    )

    course = models.ForeignKey(#This creates a foreign key relationship to the Course model, indicating that each attendance record is associated with a specific course.
        Course,
        on_delete=models.CASCADE,#This means that if a course is deleted, all its associated attendance records will also be deleted.
        related_name="attendance_records"#This means that you can access the attendance records of a course using course.attendance_records
    )

    date = models.DateField()#This defines a date field to store the date of the attendance record.
    status = models.CharField(#This defines a character field to store the attendance status (Present, Absent, or Late) for the student on the given date.
        max_length=10,
        choices=STATUS_CHOICES
    )

    class Meta:
        ordering = ["-date"]#This specifies that attendance records should be ordered by the most recent date first when retrieved from the database.
        unique_together = ["student", "course", "date"]#This ensures that there can only be one attendance record for a specific student, course, and date combination, preventing duplicate entries.

    def __str__(self):
        return f"{self.student} - {self.course} - {self.date}"