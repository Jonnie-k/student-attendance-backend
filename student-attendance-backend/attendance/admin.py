from django.contrib import admin
from .models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "date", "status")
    list_filter = ("status", "course", "date")
    search_fields = ("student__user__username",)