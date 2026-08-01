# Student Attendance System — Frontend

A Django web application that serves as the user interface for the Student Attendance Management System. It communicates with the [backend REST API](https://student-attendance-backend-h3hr.onrender.com/api) to manage students, teachers, courses, attendance records, and generate reports.

**Live Demo:** https://student-attendance-frontend-mupu.onrender.com

---

## Features

- Dashboard — Overview of total students, teachers, courses, and attendance records
- Students — Add, edit, delete, and search students
- Teachers — Add, edit, delete, and search teachers
- Courses — Add, edit, delete, and search courses with teacher assignment
- Attendance — Record, edit, delete, and search attendance per student per course
- Reports** — Filter attendance by student, course, date, and status with summary statistics
- Authentication** — Login/logout with session-based auth and protected routes

---

### Tech Stach
- **Frontend Framework:** Django
-Python
-Django REST framework
-PostgreSQL
-HTML
-CSS
-Render
-Github

## URL Routes

| URL | View | Description |
|---|---|---|
| `/` | `home` | Dashboard |
| `/accounts/login/` | `CustomLoginView` | Login page |
| `/accounts/logout/` | `CustomLogoutView` | Logout |
| `/students/` | `students` | List all students |
| `/students/add/` | `add_student` | Add a student |
| `/students/edit/<id>/` | `edit_student` | Edit a student |
| `/students/delete/<id>/` | `delete_student` | Delete a student |
| `/teachers/` | `teachers` | List all teachers |
| `/teachers/add/` | `add_teacher` | Add a teacher |
| `/teachers/edit/<id>/` | `edit_teacher` | Edit a teacher |
| `/teachers/delete/<id>/` | `delete_teacher` | Delete a teacher |
| `/courses/` | `courses` | List all courses |
| `/courses/add/` | `add_course` | Add a course |
| `/courses/edit/<id>/` | `edit_course` | Edit a course |
| `/courses/delete/<id>/` | `delete_course` | Delete a course |
| `/attendance/` | `attendance` | List attendance records |
| `/attendance/add/` | `add_attendance` | Add attendance record |
| `/attendance/edit/<id>/` | `edit_attendance` | Edit attendance record |
| `/attendance/delete/<id>/` | `delete_attendance` | Delete attendance record |
| `/reports/` | `reports` | Attendance reports & statistics |

---

## Backend API

This frontend connects to the backend REST API at:
https://student-attendance-backend-h3hr.onrender.com/api

Endpoints used:

| Endpoint | Description |
|---|---|
| `/api/students/` | CRUD for students |
| `/api/teachers/` | CRUD for teachers |
| `/api/courses/` | CRUD for courses |
| `/api/attendance/` | CRUD for attendance records |

---

## License

MIT

## Author
John Mulwa King'oo