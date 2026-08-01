#!/usr/bin/env bash
# Render build script for the backend.
# Exit immediately if any command fails.
set -o errexit

pip install -r requirements.txt

# Collect static files (admin CSS/JS, DRF browsable-API assets, etc.)
# into STATIC_ROOT so WhiteNoise can serve them.
python manage.py collectstatic --no-input

# Apply any outstanding database migrations.
python manage.py migrate
