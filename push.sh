#!/usr/bin/env bash
# Usage: ./push.sh "your commit message"
set -e

ROOT="$(cd "$(dirname "$0")" && pwd)"
MESSAGE="${1:-"Update: $(date '+%Y-%m-%d %H:%M:%S')"}"

echo ">>> Collecting static files (frontend)..."
cd "$ROOT/student-attendance-frontend"
python manage.py collectstatic --noinput

echo ">>> Committing and pushing to GitHub..."
cd "$ROOT"
git add .
git commit -m "$MESSAGE"
git push origin main

echo ">>> Done!"
