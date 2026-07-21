from django.contrib import admin
from .models import Student

# Register your models here.

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("admission_number", "user", "phone_number", "gender")
    search_fields = ("admission_number", "user__username", "user__first_name")
    list_filter = ("gender",)