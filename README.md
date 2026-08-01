# Student Attendance Management System

## Features
- User Authentication
- Student Management
- Teacher Management
- Course Management
- Attendance Tracking
- REST APIs
- Docker Support

## Tech Stack
- Python
- Django
- Django REST Framework
- SQLite
- Docker

## Installation

git clone ...

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver

## Docker

docker build -t student-attendance-backend .

docker run -p 8000:8000 student-attendance-backend

## API Endpoints

/api/students/
/api/teachers/
/api/courses/
/api/attendance/