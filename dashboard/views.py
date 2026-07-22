from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, "home/index.html")


@login_required
def dashboard(request):
    if request.user.is_superuser:
        return render(request, "dashboard/admin_dashboard.html")

    if hasattr(request.user, "teacher"):
        return render(request, "dashboard/teacher_dashboard.html")

    if hasattr(request.user, "student"):
        return render(request, "dashboard/student_dashboard.html")

    return render(request, "dashboard/admin_dashboard.html")