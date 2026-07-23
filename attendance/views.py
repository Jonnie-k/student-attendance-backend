from rest_framework import viewsets
from .models import Attendance
from .serializers import AttendanceSerializer


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all().order_by("id")
    serializer_class = AttendanceSerializer