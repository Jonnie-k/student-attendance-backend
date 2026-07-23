from rest_framework import serializers
from .models import Teacher


class TeacherSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    full_name = serializers.CharField(source="user.get_full_name", read_only=True)

    class Meta:
        model = Teacher
        fields = [
            "id",
            "user",
            "username",
            "full_name",
            "employee_number",
            "department",
        ]