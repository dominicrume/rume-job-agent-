#!/bin/bash
set -e

# Initialise SQLite database if it doesn't exist
python agent/db/init_db.py

# Start production WSGI server
# Railway injects PORT; fall back to 5050 locally
exec gunicorn agent.dashboard.app:app \
  --bind "0.0.0.0:${PORT:-5050}" \
  --workers 2 \
  --timeout 120 \
  --access-logfile - \
  --error-logfile -
