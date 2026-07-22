from django.contrib import admin
from .models import Student

# Register your models here.

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("admission_number", "user", "phone_number", "gender")#These are columns displayed in the admin list view for the Student model. It shows the admission number, associated user, phone number,
    search_fields = ("admission_number", "user__username", "user__first_name")#This allows the admin to search for students based on their admission number, username, or first name of the associated user.
    list_filter = ("gender",)#This adds a filter sidebar in the admin list view, allowing the admin to filter students based on their gender.