from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Student


class StudentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    full_name = serializers.CharField(source="user.get_full_name", read_only=True)

    class Meta:
        model = Student
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "full_name",
            "admission_number",
            "phone_number",
            "gender",
        ]

    def create(self, validated_data):
        user_data = validated_data.pop("user")

        user = User.objects.create(
            username=user_data["username"],
            first_name=user_data.get("first_name", ""),
            last_name=user_data.get("last_name", ""),
        )

        student = Student.objects.create(
            user=user,
            **validated_data
        )

        return student

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", None)

        if user_data:
            user = instance.user
            user.username = user_data.get("username", user.username)
            user.first_name = user_data.get("first_name", user.first_name)
            user.last_name = user_data.get("last_name", user.last_name)
            user.save()

        return super().update(instance, validated_data)

    def validate_phone_number(self, value):
        if not value.isdigit():
            raise serializers.ValidationError(
                "Phone number must contain only digits."
            )

        if len(value) < 10:
            raise serializers.ValidationError(
                "Phone number is too short."
            )

        return value

    def validate_admission_number(self, value):
        if Student.objects.filter(admission_number=value).exists():
            raise serializers.ValidationError(
                "Admission number already exists."
            )

        return value