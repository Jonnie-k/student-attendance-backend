from rest_framework import serializers
from .models import Student


class StudentSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="user.get_full_name", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Student
        fields = [
            "id",
            "user",
            "username",
            "full_name",
            "admission_number",
            "phone_number",
            "gender",
        ]

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