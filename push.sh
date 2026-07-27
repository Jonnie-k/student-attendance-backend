#!/bin/bash

# Usage: ./push.sh "your commit message"
# If no message is provided, a default timestamped message is used

set -e

ROOT="$(cd "$(dirname "$0")" && pwd)"
VENV="$ROOT/.venv/bin/python"
MESSAGE="${1:-"Update: $(date '+%Y-%m-%d %H:%M:%S')"}"

echo ">>> Collecting static files (frontend)..."
cd "$ROOT/student-attendance-frontend"
"$VENV" manage.py collectstatic --noinput

echo ">>> Committing and pushing to GitHub..."
cd "$ROOT"
git add .
git commit -m "$MESSAGE"
git push origin main

echo ">>> Done!"
