#!/usr/bin/env bash
# Render build script for the frontend.
# Exit immediately if any command fails.
set -o errexit

pip install -r requirements.txt

# Collect static files (custom CSS, admin assets, etc.) into STATIC_ROOT
# so WhiteNoise can serve them.
python manage.py collectstatic --no-input

# Apply any outstanding database migrations (auth/sessions tables).
python manage.py migrate
