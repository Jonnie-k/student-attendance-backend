from django.contrib import admin
from .models import Teacher


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("employee_number", "user", "department")
    search_fields = ("employee_number", "user__username")
    list_filter = ("department",)