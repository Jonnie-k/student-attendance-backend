import os

import requests
from dotenv import load_dotenv
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from functools import wraps

load_dotenv()

# Base URL of the backend REST API.
# Defaults to a locally running backend (python manage.py runserver on the
# default port). Override with BASE_API_URL in a .env file if you want to
# point at a deployed backend instead, e.g.:
#   BASE_API_URL=https://student-attendance-backend-h3hr.onrender.com/api
BASE_API = os.getenv("BASE_API_URL", "http://127.0.0.1:8000/api")

# Seconds to wait for the backend before giving up. Without this, a hung
# backend would hang the whole page indefinitely.
REQUEST_TIMEOUT = 10


def handle_api_errors(view_func):
    """
    Wraps a view so that connection problems with the backend API (backend
    not running, wrong URL, timeout, DNS failure, etc.) show a friendly
    "backend unavailable" page instead of an unhandled 500 error.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        try:
            return view_func(request, *args, **kwargs)
        except requests.exceptions.RequestException:
            messages.error(
                request,
                "Could not connect to the backend API. Please make sure the "
                f"backend server is running and reachable at {BASE_API}.",
            )
            return render(
                request,
                "frontend/backend_unavailable.html",
                {"base_api": BASE_API},
                status=503,
            )
    return wrapper


def safe_json(response):
    """Best-effort JSON parsing of an error response from the backend."""
    try:
        return response.json()
    except ValueError:
        return {"detail": f"Unexpected error from backend (status {response.status_code})."}


def fetch_all(url):
    """Fetch every page of a (possibly paginated) DRF list endpoint."""
    results = []
    while url:
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list):
            return data
        results.extend(data.get("results", []))
        url = data.get("next")
    return results


@login_required
@handle_api_errors
def home(request):
    students = fetch_all(f"{BASE_API}/students/")
    teachers = fetch_all(f"{BASE_API}/teachers/")
    courses = fetch_all(f"{BASE_API}/courses/")
    attendance = fetch_all(f"{BASE_API}/attendance/")

    context = {
        "student_count": len(students),
        "teacher_count": len(teachers),
        "course_count": len(courses),
        "attendance_count": len(attendance),
    }

    return render(request, "frontend/home.html", context)


# ==========================
# STUDENTS
# ==========================

@login_required
@handle_api_errors
def students(request):
    search = request.GET.get("search", "")
    students = fetch_all(f"{BASE_API}/students/")

    if search:
        search = search.lower()
        students = [
            s for s in students
            if (
                search in s.get("username", "").lower()
                or search in s.get("full_name", "").lower()
                or search in s.get("admission_number", "").lower()
            )
        ]

    return render(request, "frontend/students.html", {"students": students, "search": search})


@login_required
@handle_api_errors
def add_student(request):
    if request.method == "POST":
        data = {
            "username": request.POST.get("username"),
            "first_name": request.POST.get("first_name"),
            "last_name": request.POST.get("last_name"),
            "admission_number": request.POST.get("admission_number"),
            "phone_number": request.POST.get("phone_number"),
            "gender": request.POST.get("gender"),
        }

        response = requests.post(
            f"{BASE_API}/students/",
            json=data,
            timeout=REQUEST_TIMEOUT,
        )

        if response.status_code == 201:
            messages.success(request, "Student added successfully.")
            return redirect("students")

        return render(
            request,
            "frontend/student_form.html",
            {
                "student": data,
                "error": safe_json(response),
            },
        )

    return render(request, "frontend/student_form.html")


@login_required
@handle_api_errors
def edit_student(request, student_id):
    url = f"{BASE_API}/students/{student_id}/"

    if request.method == "POST":
        data = {
            "username": request.POST.get("username"),
            "first_name": request.POST.get("first_name"),
            "last_name": request.POST.get("last_name"),
            "admission_number": request.POST.get("admission_number"),
            "phone_number": request.POST.get("phone_number"),
            "gender": request.POST.get("gender"),
        }

        response = requests.put(url, json=data, timeout=REQUEST_TIMEOUT)

        if response.status_code == 200:
            messages.success(request, "Student updated successfully.")
            return redirect("students")

        return render(
            request,
            "frontend/student_form.html",
            {
                "student": data,
                "error": safe_json(response),
            },
        )

    response = requests.get(url, timeout=REQUEST_TIMEOUT)

    if response.status_code == 200:
        student = response.json()

        return render(
            request,
            "frontend/student_form.html",
            {
                "student": student,
            },
        )

    messages.error(request, "Student not found.")
    return redirect("students")


@login_required
@handle_api_errors
def delete_student(request, student_id):
    url = f"{BASE_API}/students/{student_id}/"

    if request.method == "POST":
        requests.delete(url, timeout=REQUEST_TIMEOUT)
        messages.success(request, "Student deleted successfully.")
        return redirect("students")

    response = requests.get(url, timeout=REQUEST_TIMEOUT)

    if response.status_code == 200:
        student = response.json()

        return render(
            request,
            "frontend/student_delete.html",
            {
                "student": student,
            },
        )

    messages.error(request, "Student not found.")
    return redirect("students")


# ==========================
# TEACHERS
# ==========================

@login_required
@handle_api_errors
def teachers(request):
    search = request.GET.get("search", "")
    teachers = fetch_all(f"{BASE_API}/teachers/")

    if search:
        search = search.lower()
        teachers = [
            t for t in teachers
            if (
                search in t.get("username", "").lower()
                or search in t.get("full_name", "").lower()
                or search in t.get("employee_number", "").lower()
                or search in t.get("department", "").lower()
            )
        ]

    return render(request, "frontend/teachers.html", {"teachers": teachers, "search": search})


@login_required
@handle_api_errors
def add_teacher(request):
    if request.method == "POST":
        data = {
            "username": request.POST.get("username"),
            "first_name": request.POST.get("first_name"),
            "last_name": request.POST.get("last_name"),
            "employee_number": request.POST.get("employee_number"),
            "department": request.POST.get("department"),
        }
        response = requests.post(
            f"{BASE_API}/teachers/",
            json=data,
            timeout=REQUEST_TIMEOUT,
        )

        if response.status_code == 201:
            messages.success(request, "Teacher added successfully.")
            return redirect("teachers")

        return render(
            request,
            "frontend/teacher_form.html",
            {
                "teacher": data,
                "error": safe_json(response),
            },
        )

    return render(request, "frontend/teacher_form.html")


@login_required
@handle_api_errors
def edit_teacher(request, teacher_id):
    url = f"{BASE_API}/teachers/{teacher_id}/"

    if request.method == "POST":
        data = {
            "username": request.POST.get("username"),
            "first_name": request.POST.get("first_name"),
            "last_name": request.POST.get("last_name"),
            "employee_number": request.POST.get("employee_number"),
            "department": request.POST.get("department"),
        }
        response = requests.put(url, json=data, timeout=REQUEST_TIMEOUT)

        if response.status_code == 200:
            messages.success(request, "Teacher updated successfully.")
            return redirect("teachers")

        return render(
            request,
            "frontend/teacher_form.html",
            {
                "teacher": data,
                "error": safe_json(response),
            },
        )

    response = requests.get(url, timeout=REQUEST_TIMEOUT)

    if response.status_code == 200:
        teacher = response.json()

        return render(
            request,
            "frontend/teacher_form.html",
            {
                "teacher": teacher,
            },
        )

    messages.error(request, "Teacher not found.")
    return redirect("teachers")


@login_required
@handle_api_errors
def delete_teacher(request, teacher_id):
    url = f"{BASE_API}/teachers/{teacher_id}/"

    if request.method == "POST":
        requests.delete(url, timeout=REQUEST_TIMEOUT)
        messages.success(request, "Teacher deleted successfully.")
        return redirect("teachers")

    response = requests.get(url, timeout=REQUEST_TIMEOUT)

    if response.status_code == 200:
        teacher = response.json()

        return render(
            request,
            "frontend/teacher_delete.html",
            {
                "teacher": teacher,
            },
        )

    messages.error(request, "Teacher not found.")
    return redirect("teachers")


# ==========================
# COURSES
# ==========================

@login_required
@handle_api_errors
def courses(request):
    search = request.GET.get("search", "")
    courses = fetch_all(f"{BASE_API}/courses/")

    if search:
        search = search.lower()
        courses = [
            c for c in courses
            if (
                search in c.get("course_name", "").lower()
                or search in c.get("course_code", "").lower()
                or search in c.get("teacher_name", "").lower()
            )
        ]

    return render(request, "frontend/courses.html", {"courses": courses, "search": search})


@login_required
@handle_api_errors
def add_course(request):
    teachers = fetch_all(f"{BASE_API}/teachers/")

    if request.method == "POST":
        data = {
            "course_name": request.POST.get("course_name"),
            "course_code": request.POST.get("course_code"),
            "teacher": request.POST.get("teacher"),
        }

        response = requests.post(
            f"{BASE_API}/courses/",
            json=data,
            timeout=REQUEST_TIMEOUT,
        )

        if response.status_code == 201:
            messages.success(request, "Course added successfully.")
            return redirect("courses")

        return render(
            request,
            "frontend/course_form.html",
            {
                "teachers": teachers,
                "course": data,
                "error": safe_json(response),
            },
        )

    return render(
        request,
        "frontend/course_form.html",
        {
            "teachers": teachers,
        },
    )


@login_required
@handle_api_errors
def edit_course(request, course_id):
    teachers = fetch_all(f"{BASE_API}/teachers/")

    url = f"{BASE_API}/courses/{course_id}/"

    if request.method == "POST":
        data = {
            "course_name": request.POST.get("course_name"),
            "course_code": request.POST.get("course_code"),
            "teacher": request.POST.get("teacher"),
        }

        response = requests.put(url, json=data, timeout=REQUEST_TIMEOUT)

        if response.status_code == 200:
            messages.success(request, "Course updated successfully.")
            return redirect("courses")

        return render(
            request,
            "frontend/course_form.html",
            {
                "teachers": teachers,
                "course": data,
                "error": safe_json(response),
            },
        )

    response = requests.get(url, timeout=REQUEST_TIMEOUT)

    if response.status_code == 200:
        course = response.json()

        return render(
            request,
            "frontend/course_form.html",
            {
                "teachers": teachers,
                "course": course,
            },
        )

    messages.error(request, "Course not found.")
    return redirect("courses")


@login_required
@handle_api_errors
def delete_course(request, course_id):
    url = f"{BASE_API}/courses/{course_id}/"

    if request.method == "POST":
        requests.delete(url, timeout=REQUEST_TIMEOUT)
        messages.success(request, "Course deleted successfully.")
        return redirect("courses")

    response = requests.get(url, timeout=REQUEST_TIMEOUT)

    if response.status_code == 200:
        course = response.json()
        return render(request, "frontend/course_delete.html", {"course": course})

    messages.error(request, "Course not found.")
    return redirect("courses")


# ==========================
# ATTENDANCE
# ==========================

@login_required
@handle_api_errors
def attendance(request):
    search = request.GET.get("search", "")
    attendance = fetch_all(f"{BASE_API}/attendance/")

    if search:
        search = search.lower()
        attendance = [
            r for r in attendance
            if (
                search in r.get("student_name", "").lower()
                or search in r.get("course_name", "").lower()
                or search in r.get("status", "").lower()
                or search in r.get("date", "").lower()
            )
        ]

    return render(request, "frontend/attendance.html", {"attendance": attendance, "search": search})


@login_required
@handle_api_errors
def add_attendance(request):
    students = fetch_all(f"{BASE_API}/students/")
    courses = fetch_all(f"{BASE_API}/courses/")

    if request.method == "POST":
        data = {
            "student": request.POST.get("student"),
            "course": request.POST.get("course"),
            "date": request.POST.get("date"),
            "status": request.POST.get("status"),
        }

        response = requests.post(
            f"{BASE_API}/attendance/",
            json=data,
            timeout=REQUEST_TIMEOUT,
        )

        if response.status_code == 201:
            messages.success(request, "Attendance record added successfully.")
            return redirect("attendance")

        return render(
            request,
            "frontend/attendance_form.html",
            {
                "attendance": data,
                "students": students,
                "courses": courses,
                "error": safe_json(response),
            },
        )

    return render(
        request,
        "frontend/attendance_form.html",
        {
            "students": students,
            "courses": courses,
        },
    )


@login_required
@handle_api_errors
def edit_attendance(request, attendance_id):
    students = fetch_all(f"{BASE_API}/students/")
    courses = fetch_all(f"{BASE_API}/courses/")

    url = f"{BASE_API}/attendance/{attendance_id}/"

    if request.method == "POST":
        data = {
            "student": request.POST.get("student"),
            "course": request.POST.get("course"),
            "date": request.POST.get("date"),
            "status": request.POST.get("status"),
        }

        response = requests.put(url, json=data, timeout=REQUEST_TIMEOUT)

        if response.status_code == 200:
            messages.success(request, "Attendance record updated successfully.")
            return redirect("attendance")

        return render(
            request,
            "frontend/attendance_form.html",
            {
                "attendance": data,
                "students": students,
                "courses": courses,
                "error": safe_json(response),
            },
        )

    response = requests.get(url, timeout=REQUEST_TIMEOUT)

    if response.status_code == 200:
        attendance = response.json()

        return render(
            request,
            "frontend/attendance_form.html",
            {
                "attendance": attendance,
                "students": students,
                "courses": courses,
            },
        )

    messages.error(request, "Attendance record not found.")
    return redirect("attendance")


@login_required
@handle_api_errors
def delete_attendance(request, attendance_id):
    url = f"{BASE_API}/attendance/{attendance_id}/"

    if request.method == "POST":
        requests.delete(url, timeout=REQUEST_TIMEOUT)
        messages.success(request, "Attendance record deleted successfully.")
        return redirect("attendance")

    response = requests.get(url, timeout=REQUEST_TIMEOUT)

    if response.status_code == 200:
        attendance = response.json()

        return render(
            request,
            "frontend/attendance_delete.html",
            {
                "attendance": attendance,
            },
        )

    messages.error(request, "Attendance record not found.")
    return redirect("attendance")


@login_required
@handle_api_errors
def reports(request):
    attendance = fetch_all(f"{BASE_API}/attendance/")

    # Get filter values
    student = request.GET.get("student", "")
    course = request.GET.get("course", "")
    status = request.GET.get("status", "")
    date = request.GET.get("date", "")

    # Apply filters
    if student:
        attendance = [
            record for record in attendance
            if student.lower() in record.get("student_name", "").lower()
        ]

    if course:
        attendance = [
            record for record in attendance
            if course.lower() in record.get("course_name", "").lower()
        ]

    if status:
        attendance = [
            record for record in attendance
            if record.get("status") == status
        ]

    if date:
        attendance = [
            record for record in attendance
            if record.get("date") == date
        ]

    total_records = len(attendance)

    present_count = sum(
        1 for record in attendance
        if record.get("status") == "Present"
    )

    absent_count = sum(
        1 for record in attendance
        if record.get("status") == "Absent"
    )

    late_count = sum(
        1 for record in attendance
        if record.get("status") == "Late"
    )

    attendance_percentage = (
        (present_count / total_records) * 100
        if total_records else 0
    )

    context = {
        "attendance": attendance,
        "total_records": total_records,
        "present_count": present_count,
        "absent_count": absent_count,
        "late_count": late_count,
        "attendance_percentage": round(attendance_percentage, 1),

        "student": student,
        "course": course,
        "status": status,
        "date": date,
    }

    return render(
        request,
        "frontend/reports.html",
        context,
    )
