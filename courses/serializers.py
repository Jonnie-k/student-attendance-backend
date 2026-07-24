from rest_framework import serializers
from .models import Course


class CourseSerializer(serializers.ModelSerializer):
    teacher_name = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            "id",
            "course_name",
            "course_code",
            "teacher",
            "teacher_name",
        ]

    def get_teacher_name(self, obj):
        full_name = obj.teacher.user.get_full_name()

        if full_name:
            return full_name

        return obj.teacher.user.username