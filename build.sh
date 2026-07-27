#!/usr/bin/env bash
set -e

cd student-attendance-frontend
pip install -r requirements.txt
python manage.py migrate --noinput
python manage.py collectstatic --noinput
