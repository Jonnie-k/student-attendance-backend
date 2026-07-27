from rest_framework import serializers
from .models import Attendance


class AttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    course_name = serializers.CharField(
        source="course.course_name",
        read_only=True,
    )

    class Meta:
        model = Attendance
        fields = [
            "id",
            "student",
            "student_name",
            "course",
            "course_name",
            "date",
            "status",
        ]

    def get_student_name(self, obj):
        full_name = obj.student.user.get_full_name()

        if full_name:
            return full_name

        return obj.student.user.username