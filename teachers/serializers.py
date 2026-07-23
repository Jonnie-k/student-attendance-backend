from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Teacher


class TeacherSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    first_name = serializers.CharField(
        source="user.first_name",
        required=False,
        allow_blank=True,
    )
    last_name = serializers.CharField(
        source="user.last_name",
        required=False,
        allow_blank=True,
    )
    full_name = serializers.CharField(
        source="user.get_full_name",
        read_only=True,
    )

    class Meta:
        model = Teacher
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "full_name",
            "employee_number",
            "department",
        ]

    def create(self, validated_data):
        user_data = validated_data.pop("user")

        user = User.objects.create(
            username=user_data.get("username"),
            first_name=user_data.get("first_name", ""),
            last_name=user_data.get("last_name", ""),
        )

        teacher = Teacher.objects.create(
            user=user,
            **validated_data
        )

        return teacher

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})

        user = instance.user
        user.username = user_data.get("username", user.username)
        user.first_name = user_data.get("first_name", user.first_name)
        user.last_name = user_data.get("last_name", user.last_name)
        user.save()

        instance.employee_number = validated_data.get(
            "employee_number",
            instance.employee_number,
        )

        instance.department = validated_data.get(
            "department",
            instance.department,
        )

        instance.save()

        return instance