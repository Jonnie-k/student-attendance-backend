from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    # Students
    path("students/", views.students, name="students"),
    path("students/add/", views.add_student, name="add_student"),
    path("students/edit/<int:student_id>/", views.edit_student, name="edit_student"),
    path("students/delete/<int:student_id>/", views.delete_student, name="delete_student"),

    # Teachers
    path("teachers/", views.teachers, name="teachers"),
    path("teachers/add/", views.add_teacher, name="add_teacher"),
    path("teachers/edit/<int:teacher_id>/", views.edit_teacher, name="edit_teacher"),
    path("teachers/delete/<int:teacher_id>/", views.delete_teacher, name="delete_teacher"),

    # Courses
    path("courses/", views.courses, name="courses"),
    path("courses/add/", views.add_course, name="add_course"),
    path("courses/edit/<int:course_id>/", views.edit_course, name="edit_course"),
    path("courses/delete/<int:course_id>/", views.delete_course, name="delete_course"),

    # Attendance
    path("attendance/", views.attendance, name="attendance"),
    path("attendance/add/", views.add_attendance, name="add_attendance"),
    path("attendance/edit/<int:attendance_id>/", views.edit_attendance, name="edit_attendance"),
    path("attendance/delete/<int:attendance_id>/", views.delete_attendance, name="delete_attendance"),

    # Reports
    path("reports/", views.reports, name="reports"),
]